from utils import extract_data_from_csv, WALLET_AMOUNT, display_result
import datetime

FICHIER = "test_shares.csv"


def list_combinaisons(data):
    """
    Fonction qui liste les combinaisons possibles.
    :param data: ensemble des données sur les actions.
    :type data: list <tuple <x> >.
    :return: liste de combinaisons.
    :rtype: list <list <bool>>
    """
    combinaisons = []
    size = 2 ** len(data)
    print("Listing, Please wait")
    for i in range(size):
        print("\033[1F" + "Listing", format(i / size, '.2'), "%")
        # calcul de la representation binaire du numero de la combinaison
        bin_value = bin(i)[2:]
        # codage sur len(data) bits
        bin_value = '0' * (len(data) - len(bin_value)) + bin_value

        # on calcule la combinaison avec les actions que l'on prend sur l'ensemble des actions (n bites)
        combinaison = []
        for j in range(len(bin_value)):
            # ATTENTION bin_value est un string donc un doit comparer le bit en tant que string (== '1')
            # pour la combinaison i indique si l'on prend l'action j
            combinaison.append(bin_value[j] == '1')

        combinaisons.append(combinaison)

    return combinaisons


def find_best_combinaison(combinaisons, FICHIER):
    """
    Fonction qui permet de retourner la meilleur combinaison.
    :param combinaisons: Ensemble des combinaisons possible.
    :type combinaisons: list <list <bool>>.
    :param FICHIER: Nom du fichier.
    :type FICHIER: str.
    :return: Resultat de l'investissement choisi.
    :rtype:list <x>.
    """
    result_combinaison = []
    i = 0
    size = len(combinaisons)
    print("Evaluating")
    for i in range(len(combinaisons)):
        combinaison = combinaisons[i]
        print("Evaluating", format(i / size, '.2'))

        wallet_depart = WALLET_AMOUNT
        wallet_euro = WALLET_AMOUNT
        wallet = []
        gain = 0
        finished = True  # si la solution finie ou pas
        data_csv = extract_data_from_csv(FICHIER)
        for picked, action_data in zip(combinaison, data_csv):
            name, prix, rent = action_data
            if picked:
                wallet.append(action_data)
                if prix < wallet_euro:
                    wallet_euro -= prix
                    gain += prix * (rent / 100)
                else:
                    # on en peut pas l'acheter donc la solution n'est pas valide
                    finished = False
                    break
        result_combinaison.append((wallet, finished, None if not finished else gain, wallet_depart - wallet_euro))
        i += 1

    filter_result = [combinaison for combinaison in result_combinaison if
                     # on ne garde que celles qui ont finies
                     combinaison[1]]
    # on trie les combinaisons par ordre décroissant de gain
    sorted_result = sorted(filter_result, key=lambda x: -x[2])

    return sorted_result[0]


t = datetime.datetime.now()

display_result(
    find_best_combinaison(
        list_combinaisons(
            extract_data_from_csv(FICHIER)
        ),
        FICHIER
    )
)
print("-- Brute force solution --")
print("temps", datetime.datetime.now() - t)

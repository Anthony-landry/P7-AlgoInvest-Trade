WALLET_AMOUNT = 500


def extract_data_from_csv(fichier):
    """
    Fonction qui permet de retourner les données extraites du fichier CSV donné en parametre
    :param fichier: nom du fichier.
    :type fichier: str
    :return: liste des actions
    :rtype: list <tuple <x> >
    """
    # lecture du fichier csv
    filename = "data/" + fichier
    f = open(filename, "r")
    lines = f.readlines()
    lines = lines[1:]  # enlever la ligne d'entete
    f.close()

    # traitement des données list<tuple<str, float, float>>
    data = []
    for line in lines:
        line = line.split("\n")[0]  # enlever le saut de ligne
        triplet = line.split(",")
        if float(triplet[1]) > 0:
            data.append((triplet[0], float(triplet[1]), float(triplet[2])))
    return data


def display_result(res):
    """
    Fonction qui affiche le résultat.
    :param res: resultat de l'investissement choisi.
    :type res: list <x>
    """
    print("Wallet")
    print("\t", "Nom\t\t\tPrix\t\tRendement (2 ans)")
    for action in res[0]:
        action = list(action)
        action[1] = str(action[1]) + " €"
        action[2] = str(action[2]) + " %"
        print("\t", "\t\t".join([str(i) for i in action]))
    print("Gain final", "%.2f" % res[2], "€")
    print("Rent moy sur 2 ans", "%.2f" % (res[2] / (res[3]) * 100), "%")


"""
from joblib import Parallel, delayed
results = Parallel(n_jobs=2)(delayed(process)(i) for i in range(10))
"""

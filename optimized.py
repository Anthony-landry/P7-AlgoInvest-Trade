from utils import extract_data_from_csv, WALLET_AMOUNT, display_result
from tqdm import tqdm
import datetime

FICHIER = "dataset2_Python+P7.csv"


def gain_for_1euro_invested(x):
    """
    Fonction qui permet de retourner le rendement normalisé pour une action aynt un cours positive.
    :param x: les données d'une action.
    :type x: tuple.
    :return: rendement normalisé.
    :rtype: float.
    """
    return (x[1] * x[2] / 100) / x[1] if x[1] != 0 else 0  # pour 1€ invest combien j'en récupère


def find_best_solution_glouton(data):
    """
    :param data: Ensemble des données sur les actions.
    :type data: list <tuple <x> >
    :return: La liste des actions achetées, indique si la solution a finie ou pas,
    le gain effectué, le reste du portefeuille.
    :rtype: tuple <x>
    """
    # on augmente les données pour ajouter une nouvelle métrique
    # qui calcule combien d'euro sont gagné pour 1 euro d'investi
    # on ne garde que les actions réelles qui ont prix > 0
    data_augmented = [(d[0], d[1], d[2], gain_for_1euro_invested(d)) for d in data if d[1] > 0]

    # on tri les actions pour récupérer celle qui permette d'obtenir le plus par euro investi.
    # meilleur algo de tri : O(n log n).
    # data_sorted = [i for i in reversed(sorted(data_augmented, key=lambda x: x[3]) if i[1] > 0]

    # on ne prend pas les actions qui n'ont pas de prix
    data_sorted = list(reversed([d[0:3] for d in sorted(data_augmented, key=lambda x: x[3])]))

    # choix de la meilleur combinaison d'actions
    wallet_depart = WALLET_AMOUNT
    wallet_euro = WALLET_AMOUNT
    wallet = []
    gain = 0

    for action in tqdm(data_sorted):  # --> n parcours
        name, prix, rent = action
        if prix < wallet_euro:
            wallet_euro -= prix
            gain += prix * rent / 100
            # wallet.append(name)
            wallet.append(action)

    return wallet, True, gain, wallet_depart - wallet_euro


t = datetime.datetime.now()
print("-- Optimized solution --")
display_result(find_best_solution_glouton(extract_data_from_csv(FICHIER)))
print("temps", datetime.datetime.now() - t)

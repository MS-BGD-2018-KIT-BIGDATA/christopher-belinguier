import requests
import re
import json
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup


""" https://www.open-medicaments.fr/#/search ==> Ibuprofene
laboratoire, equivalent traitement, annee, mois, prix, age, poids"""


def get_details(url):
    res = requests.get(url)
    page_text = res.text.encode('utf-8').decode('ascii', 'ignore')
    infos = json.loads(page_text)
    return infos

def get_ibuprofene(url):
    res = requests.get(url)
    page_text = res.text.encode('utf-8').decode('ascii', 'ignore')
    infos = json.loads(page_text)
    return infos


if __name__ == '__main__':
    infos = get_ibuprofene("https://www.open-medicaments.fr/api/v1/medicaments?query=ibuprofene")
    fichier = []
    for info in infos:
        codeCIS = info['codeCIS']
        url_medicament = "https://www.open-medicaments.fr/api/v1/medicaments/" + str(codeCIS)
        details = get_details(url_medicament)
        labo = details['titulaires']
        codeSubstance = details['compositions'][0]['substancesActives'][0]['codeSubstance']
        if codeSubstance == "02092":
            qte = details['compositions'][0]['substancesActives'][0]['dosageSubstance']
        else:
            qte = 0
        annee = details['dateAMM'][0:4]
        mois = details['dateAMM'][5:7]
        presentations = details['presentations']
        prix = presentations[0]['prix']
        age_info = re.search(r"[0-9][0-9][0-9]? ?ans", details['indicationsTherapeutiques'])
        if age_info:
            age = age_info[0]
        else:
            age = ''
        poids_info = re.search(r"[0-9][0-9][0-9]? ?kg", details['indicationsTherapeutiques'])
        if poids_info:
            poids = poids_info[0]
        else:
            poids = ''
        fichier.append([labo, qte, annee, mois, prix, age, poids])
    labels = ['labo', 'qte', 'annee', 'mois', 'prix', 'age', 'poids']
    df = pd.DataFrame.from_records(fichier, columns=labels)
    df = df.sort_values(['labo'])

    # Sauvegarde
    df.to_csv('ibuprofene.csv')


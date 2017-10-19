import requests
import re
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup


"""L'objectif est de générer un fichier de données sur le prix des Renault Zoé sur le marché de l'occasion en Ile de 
France, PACA et Aquitaine. Vous utiliserez leboncoin.fr comme source. Le fichier doit être propre et contenir les infos 
suivantes : version ( il y en a 3), année, kilométrage, prix, téléphone du propriétaire, est ce que la voiture est 
vendue par un professionnel ou un particulier. Vous ajouterez une colonne sur le prix de l'Argus du modèle que vous 
récupérez sur ce site http://www.lacentrale.fr/cote-voitures-renault-zoe--2013-.html. Les données quanti 
(prix, km notamment) devront être manipulables (pas de string, pas d'unité). Vous ajouterez une colonne si la 
voiture est plus chère ou moins chère que sa cote moyenne.﻿"""

REGIONS = ['aquitaine', 'ile_de_france', 'provence_alpes_cote_d_azur']
URL_CENTRALE = 'http://www.lacentrale.fr/cote-voitures-renault-zoe--2013-.html'
VERSION_ZOE = ['intens', 'life', 'zen']


def get_soup_from_url(url):
    try:
        req = requests.get(url)
        page_text = req.text.encode('utf-8').decode('ascii', 'ignore')
        soup = BeautifulSoup(page_text, 'html.parser')
        # soup = BeautifulSoup(req.text, 'html.parser')
        return soup

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)
    return 0


def get_nb_pages(url):
    soup = get_soup_from_url(url)
    resultats = soup.find_all("a", {"id": "last"})
    return int(re.sub(r"&brd=Renault&mdl=Zoe", "", resultats[0].get('href'))[-1])


def get_link(url):
    soup = get_soup_from_url(url)
    resultats = soup.find_all(class_='list_item')
    return [[res.get('href'), len(res.select('section > p > span'))] for res in resultats]


def get_details(link_detail):
    url = "https:" + str(link_detail[0])
    soup = get_soup_from_url(url)
    details = soup.find_all(class_='value')
    # detail
    prix = float(re.sub(r"\D", "", details[0].text))
    annee = int(re.sub(r"\D", "", details[4].text))
    kilometrage = int(re.sub(r"\D", "", details[5].text))
    vendeur = 'Professionnel' if link_detail[1] == 1 else 'Particulier'
    description = re.sub(r"\W", "", details[-1].text.lower())
    # print(description)
    version = "NaN"
    if VERSION_ZOE[0] in description:
        version = VERSION_ZOE[0]
    elif VERSION_ZOE[1] in description:
        version = VERSION_ZOE[1]
    elif VERSION_ZOE[2] in description:
        version = VERSION_ZOE[2]
    print(version)
    comparateur = "NaN"
    if version != "NaN":
        argus_key = str(annee) + '-' + str(version)
        argus = dict_argus[argus_key]
        if prix < argus:
            comparateur = True
        else:
            comparateur = False
    else:
        argus = "NaN"
    # telephone = soup.find_all(class_='phone_number')
    # print(telephone)
    return [annee, version, prix, kilometrage, vendeur, argus, comparateur]


def get_argus(year_min, year_max):
    dict_argus = {}
    for year in np.arange(year_min, year_max):
        for version in VERSION_ZOE:
            url = "https://www.lacentrale.fr/cote-auto-renault-zoe-" + version + "+charge+rapide-" + str(year) + ".html"
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            argus = int(soup.find_all('span', class_='jsRefinedQuot')[0].text.strip().replace(" ", ""))
            key = str(year) + '-' + str(version)
            dict_argus[key] = argus
    return dict_argus



if __name__ == '__main__':
    # Crawling
    for region in REGIONS:
        # Centrale
        dict_argus = get_argus(2012, 2018)

        # Le bon coin
        print("Region : " + str(region))
        nb_pages = get_nb_pages('https://www.leboncoin.fr/voitures/offres/' + str(region) + '/?o=1&brd=Renault&mdl=Zoe')
        fichier = []
        for i in range(1, nb_pages+1):
            url_region = 'https://www.leboncoin.fr/voitures/offres/' + str(region) + '/?o=' + str(i) + '&brd=Renault&mdl=Zoe'
            link_details = get_link(url_region)
            for link in link_details:
                fichier.append(get_details(link))
        print("length fichier : " + str(len(fichier)))
        labels = ['Annee', 'Version', 'Prix', 'Kilometrage', 'Vendeur', 'argus', 'comparateur']
        df = pd.DataFrame.from_records(fichier, columns=labels)
        df = df.sort_values(['Annee', 'Version', 'Prix', 'Kilometrage', 'Vendeur', 'argus', 'comparateur'])
        print(df)

        # Sauvegarde
        df.to_csv(region + '.csv')

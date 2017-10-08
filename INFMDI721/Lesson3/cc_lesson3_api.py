# -*- coding: utf-8 -*-
import sys
import requests
import googlemaps
import re
import pandas as pd
from bs4 import BeautifulSoup

"""Implementer des bureaux commerciaux en france. Touver la distance entre les 100 plus grandes villes de france. Renvoyer un csv."""

URL_CITIES = "https://lespoir.jimdo.com/2015/03/05/classement-des-plus-grandes-villes-de-france-source-insee/"


def get_token(path):
    f = open(path, 'r')
    my_token = str(f.read())
    return my_token


def get_soup_from_url(url):
    try:
        req = requests.get(url)
        page_text = req.text.encode('utf-8').decode('ascii', 'ignore')
        soup = BeautifulSoup(page_text, 'html.parser')
        return soup

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)
    return 0


def get_cities(nb):
    soup_cities = get_soup_from_url(URL_CITIES)
    td_cities = soup_cities.select("tr > td:nth-of-type(2)")
    # selected = [soup.select("table:nth-of-type(1) > tbody:nth-of-type(1) > tr:nth-of-type(" + str(2 + i) + ") > td:nth-of-type(2)")[0].text.strip() for i in range(MAX_VILLE)]
    return [re.sub(r"\W", "", td.text) for td in td_cities[1:nb+1]]


def get_distance_matrix(cities):
    maps = googlemaps.Client(key=my_token)
    return maps.distance_matrix(origins=cities, destinations=cities)


if __name__ == '__main__':
    # Variable IN
    if len(sys.argv) == 3:
        nb_cities = int(sys.argv[1])
        path_result = str(sys.argv[2])
    else:
        nb_cities = 10
        path_result = 'distances.csv'
    # Get token
    my_token = get_token('/Users/christopherbelinguier/github/token_google.txt')
    # Crawling
    cities = get_cities(nb_cities)
    print(cities)
    # API google
    distance_matrix = get_distance_matrix(cities)
    print(distance_matrix)
    df = pd.DataFrame(columns=cities, index=cities)
    for idx, row in enumerate(distance_matrix["rows"]):
        for idy, elem in enumerate(row["elements"]):
            df.at[cities[idx], cities[idy]] = elem["distance"]["text"]
    print(df)
    df.to_csv(path_result)

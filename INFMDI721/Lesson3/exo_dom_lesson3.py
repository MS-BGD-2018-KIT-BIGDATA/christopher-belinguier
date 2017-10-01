#!/usr/bin/python3.4

import requests
import re
from bs4 import BeautifulSoup


def get_soup_from_url(my_url, my_class):
    res = requests.get(my_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    res = soup.find_all(class_=my_class)
    euros_hab = [int(val.parent.select_one("td:nth-of-type(2)").text.replace('\xa0', '').replace(' ', '')) for val in res if re.search('= [ABCD]\Z', val.text)]
    # print("euros_hab : " + str(euros_hab))
    moyenne_strate = [int(val.parent.select_one("td:nth-of-type(3)").text.replace('\xa0', '').replace(' ', '')) for val in res if re.search('= [ABCD]\Z', val.text)]
    # print("moyenne_strate : " + str(moyenne_strate))
    return euros_hab, moyenne_strate





def comptes_paris(start, end):
    dic_euros_hab = {}
    dic_moyenne_strate = {}
    for year in range(start, end):
        url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=' + str(year)
        class_name = 'libellepetit G'
        euros_hab, moyenne_strate = get_soup_from_url(url, class_name)
        dic_euros_hab[year] = euros_hab
        dic_moyenne_strate[year] = moyenne_strate
    print("Euros par habitant de " + str(start) + " a " + str(end) + " : \n" + str(dic_euros_hab))
    print("Moyenne de la strate de " + str(start) + " a " + str(end) + " : \n" + str(dic_moyenne_strate))


comptes_paris(2010, 2016)

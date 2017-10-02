import requests
import numpy as np
from bs4 import BeautifulSoup


"""Pourcentage de reduction entre dell et acer sur cdiscount"""


def get_soup_from_url(my_url, my_class):
    res = requests.get(my_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup


def compute_discount(brand):
    """Attention il faut voir si prix reduit ou pas si oui calculer la diff sinon 0 + recuperer id produit.
    Voir comment se naviguer dans un dom avec les bonnes methodes. (.param pour remonter dans les parents)"""
    for num_page in range(1,30):
        url = "https://www.cdiscount.com/informatique/ordinateurs-pc-portables/pc-portables/lf-228394_6-" + brand + ".html#_his_";
        list_discount = []
        soup = get_soup_from_url(url, 'prdtBZPrice')
        if soup:
            price = soup.find_all(class_='prdtPrice')
            for val in price:
                price = float(val.text.replace('\xa0', '').replace('\u20ac', '.').replace(' ', '').replace(',', '.'))
                if val.parent.select_one("[class~=prdtPrSt]"):
                    old_price = float(val.parent.select("[class~=prdtPrSt]")[0].text.replace('\xa0', '').replace('\u20ac', '.').replace(' ', '').replace(',', '.'))
                    discount = (old_price - price)/old_price
                    list_discount.append(discount)
                else:
                    list_discount.append(0)
            average_discount = np.average(list_discount) * 100
            return round(average_discount, 2)
        else:
            return 0


print("Average discount on Acer computer : " + str(compute_discount('acer')) + "%")
print("Average discount on Dell computer : " + str(compute_discount('dell')) + "%")

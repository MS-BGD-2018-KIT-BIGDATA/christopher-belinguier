import requests
from bs4 import BeautifulSoup


"""Pourcentage de reduction entre dell et acer sur cdiscount"""


def get_soup_from_url(my_url, my_class):
    res = requests.get(my_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    res = soup.find_all(class_=my_class)
    clean_res = res
    return clean_res


def best_discount(url):
    """Attention il faut voir si prix reduit ou pas si oui calculer la diff sinon 0 + recuperer id produit.
    Voir comment se naviguer dans un dom avec les bonnes methodes. (.param pour remonter dans les parents)"""
    class_name_discount = 'prdtPrSt'
    class_name_price = 'price'
    discount = get_soup_from_url(url, class_name_discount)
    print(discount)
    price = get_soup_from_url(url, class_name_price)
    print(price)
    # avg_percentage = (price - discount)/number
    # print(diff)
    # return


url_acer = "https://www.cdiscount.com/informatique/ordinateurs-pc-portables/pc-portables/lf-228394_6-acer.html#_his_"
url_dell = "https://www.cdiscount.com/informatique/ordinateurs-pc-portables/pc-portables/lf-228394_6-dell.html#_his_"

best_discount(url_acer)
best_discount(url_dell)

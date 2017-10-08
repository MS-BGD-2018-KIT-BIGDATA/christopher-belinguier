import requests
import json
import pandas as pd
from bs4 import BeautifulSoup


def get_token(path):
    f = open(path, 'r')
    my_token = str(f.read())
    return my_token


def get_soup_from_url(my_url):
    res = requests.get(my_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup


def getStarsContributor(contributor):
    # token needs to be regenerated each time : https://github.com/settings/tokens
    my_headers = {'Authorization': 'token {}'.format(my_token)}
    repo_url = 'https://api.github.com/users/' + contributor + '/repos'
    res = requests.get(repo_url, headers=my_headers)
    assert res.status_code == 200
    repositories = json.loads(res.text)
    nb_repos = len(repositories)
    if nb_repos == 0:
        return 0
    else:
        nb_stars = 0
        for repo in repositories:
            try:
                nb_stars += repo['stargazers_count']
            except ValueError:
                print('Value is not int')
        avg = round(float(nb_stars) / float(nb_repos), 2)
        return avg


def find_contributors(url):
    """Récupérer via crawling la liste des 256 top contributors sur cette page https://gist.github.com/paulmillr/2657075 """
    soup = get_soup_from_url(url)
    list_contributors = []
    if soup:
        res_search = soup.find_all(scope="row")
        for val in res_search:
            contributor = val.parent.select('a')[0].text.replace('\xa0', '').replace('\u20ac', '.').replace(' ', '').replace(',', '.')
            star_contributor = getStarsContributor(contributor)
            list_contributors.append([contributor, star_contributor])
        return list_contributors
    else:
        return 0


if __name__ == '__main__':
    my_token = get_token('/Users/christopherbelinguier/github/token_git.txt')
    url = 'https://gist.github.com/paulmillr/2657075'
    list_contributors = find_contributors(url)
    print(list_contributors)
    labels = ['Contributor', 'AverageStars']
    df = pd.DataFrame.from_records(list_contributors, columns=labels)
    df = df.sort_values('AverageStars', ascending=False)
    df

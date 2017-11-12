# coding: utf8

import pandas as pd
import numpy as np


def clean(x):
    return str(x).split('- ')[1]

# POPULATION FRANCAISE / DENSITE /100 000 hab.
df = pd.read_csv('med_gen.csv', sep=';',
                 usecols=['DEPARTEMENT', 'POPULATION FRANCAISE', 'DENSITE /100 000 hab.'],
                 converters={'DEPARTEMENT': clean})

print('\n', df.corr(method='pearson'), '\n\n')

# DENSITE / DEPASSEMENTS
df2 = pd.read_csv('med_gen.csv', sep=';', usecols=['DENSITE /100 000 hab.', 'DEPASSEMENTS (Euros)'])
print(df2.corr(method='pearson'), '\n\n')

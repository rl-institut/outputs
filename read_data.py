# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 13:31:23 2016

@author: caro
"""

import pandas
import numpy as np

from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, \
    Plot, Figure, Package, Matrix
from pylatex.utils import italic

doc = Document()
data = pandas.read_csv('energysystem/storage_soc.csv')

#print(data)
print(data['val'])


# nur Beispiel
a = np.arange(6) # erzeugt Beispiel-Array
b = a.reshape((2,3))

print(b)


# schon unsere Daten

data_matrix = data['val'].reshape((24, 365))

print(data_matrix)

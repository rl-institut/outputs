"""
Created on Tue Jul 19 2016

@author: chrischna
"""
import shapely

import pandas
import numpy as np
import matplotlib.pyplot as plt

from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, \
    Plot, Figure, Package, Matrix
from pylatex.utils import italic

doc = Document()
data = pandas.read_csv('energysystem/storage_soc.csv')

#print(data)
print(data['val'])

# unsere Daten
print(data['val'].max())
print(data['val'].min())
data_matrix = data['val'].reshape((24, 365))
#data_matrix = data['val'].reshape((365, 24))

print(data_matrix)

z = data_matrix
print(z.shape)

z_min, z_max = -np.abs(z).min(), np.abs(z).max()

plt.imshow(z, cmap='RdBu', vmin=z_min, vmax=z_max,
           interpolation='nearest', aspect='auto', origin='lower')
plt.title('Jahreswerte')
#plt.colorbar('winter')
clb = plt.colorbar()
#clb.set_label()

plt.show()

# Plot image
plt.imshow(z, cmap='afmhot', interpolation='nearest',
     origin='lower', aspect='auto', vmin=z_min, vmax=z_max)

plt.show()
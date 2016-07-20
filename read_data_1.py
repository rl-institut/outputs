# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 13:31:23 2016

@author: caro
"""

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


# nur Beispiel
a = np.arange(6) # erzeugt Beispiel-Array
b = a.reshape((2,3))

print(b)


# schon unsere Daten
print(data['val'].max())
print(data['val'].min())
data_matrix = data['val'].reshape((24, 365))
#data_matrix = data['val'].reshape((365, 24))

print(data_matrix)

# make these smaller to increase the resolution
dx, dy = 0.15, 0.05

# generate 2 2d grids for the x & y bounds
y, x = np.mgrid[slice(0, 800 + dy, dy),
                slice(0, 800 + dx, dx)]
z = data_matrix
print(z.shape)
# x and y are bounds, so z should be the value *inside* those bounds.
# Therefore, remove the last value from the z array.
#z = z[0, 364]
z = z[:-1, :-1]
print(z.shape)
z_min, z_max = -np.abs(z).min(), np.abs(z).max()


#plt.subplot(2, 2, 1)
#plt.pcolor(x, y, z, cmap='RdBu', vmin=z_min, vmax=z_max)
#plt.title('pcolor')
#set the limits of the plot to the limits of the data
#plt.axis([x.min(), x.max(), y.min(), y.max()])
#plt.colorbar()


#plt.subplot(2, 2, 2)
#plt.pcolormesh(x, y, z, cmap='RdBu', vmin=z_min, vmax=z_max)
#plt.title('pcolormesh')
## set the limits of the plot to the limits of the data
##plt.axis([x.min(), x.max(), y.min(), y.max()])
#plt.colorbar()


#plt.subplot(2, 2, 3)
plt.imshow(z, cmap='RdBu', vmin=z_min, vmax=z_max,
           extent=[x.min(), x.max(), y.min(), y.max()],
           interpolation='nearest', origin='lower')
plt.title('Jahreswerte')
plt.colorbar()

#ax = plt.subplot(2, 2, 4)
#ax.pcolorfast(x, y, z, cmap='RdBu', vmin=z_min, vmax=z_max)
#plt.title('pcolorfast')
#plt.colorbar()


plt.show()
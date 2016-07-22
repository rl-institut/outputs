"""
Created on Tue Jul 19 2016

@author: chrischan
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def read_in_data_and_plot(val):
    '''reads in time axis data, brings them to a nice matrix form
    and plots them into a diagram'''
    doc = Document()
    data = pandas.read_csv('energysystem/storage_soc.csv')

    #shows the minima and maxima
    print(data['val'].max())
    print(data['val'].min())

    #brings the data in a matrix form hours above days
    data_matrix = data['val'].reshape((24, 365))
    a = np.transpose(data_matrix)

    print(data_matrix)

    #show image of the data
    plt.imshow(a, cmap = 'inferno', interpolation='nearest', origin='lower',
    aspect = 'auto', vmin=a_min, vmax=a_max,)

    ax = plt.subplots()

    plt.title('hous of the year')
    ax.set_xlabel('Jahrestage')
    ax.set_ylabel('Tagesstunden')
    clb = plt.colorbar()
    clb.set_label('val')
    plt.show()
    return




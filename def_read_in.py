"""
Created on Tue Jul 19 2016

@author: chrischan
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def read_in_data(val):
    '''reads in time axis data, brings them to a nice matrix form
    and plots them into a diagram'''
    doc = Document()
    data = pandas.read_csv()

    #shows the minima and maxima
    print(data['val'].max())
    print(data['val'].min())

    #brings the data in a matrix form
    data_matrix = data['val'].reshape((24, 365))


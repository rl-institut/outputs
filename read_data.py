# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 13:31:23 2016

@author: caro
"""

import pandas

data = pandas.read_csv('energysystem/storage_soc.csv')

print(data)
print(data['val'])
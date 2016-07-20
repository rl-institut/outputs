
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Daten einlesen

#transform to matrix
matrix_wind = []
matrix_wind = np.reshape(df.v_wind, (365, 24))
a = np.transpose(matrix_wind)

#plt.scatter(a)
#plt.show()

print(a)

#show image of the data
plt.imshow(a, cmap = 'inferno', interpolation='nearest', origin='lower', aspect = 'auto'
,vmax=3)

plt.title('Wittenberg 2010 (v_wind)')
ax.set_xlabel('Jahrestage')
ax.set_ylabel('Tagesstunden')
clb = plt.colorbar()
clb.set_label('v_wind in m/s')
plt.show()
import numpy as np
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dados = []
with open('dataset.csv', newline='') as f:
    reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
    for row in reader:
        for i in row:
            if i != 'Minimo' and  i !="Media" and i !="Maximo" :
                dados.append(i)

metricas = ['Minimo','Media','Maximo','Minimo','Media','Maximo','Minimo','Media','Maximo','Minimo','Media','Maximo']

# set plot size for the plot
plt.rcParams["figure.figsize"] = (8, 8)

# create the plot space upon which to plot the data
fig, ax = plt.subplots()


# add the x-axis and the y-axis to the plot
ax.plot(metricas, dados)
plt.title('Request mais rápido e mais demorado')
plt.xlabel('Medidas de resultado')
plt.ylabel(' Ping (mms)')
plt.show()
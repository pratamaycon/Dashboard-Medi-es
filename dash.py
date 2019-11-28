
##import pandas as pd
##from matplotlib import pyplot as plt
##from matplotlib import style 
import numpy as np
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dados =[]
with open('dataset.csv', newline='') as f:
    reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
    for row in reader:
        for i in row:
            if i != 'Minimo' and  i !="Media" and i !="Maximo" :
                dados.append(i)

metricas = ['Minimo1','Media1','Maximo1','Minimo2','Media2','Maximo2','Minimo3','Media3','Maximo3','Minimo4','Media4','Maximo4']
x =np.arange(len(metricas))
# set plot size for the plot
plt.rcParams["figure.figsize"] = (10, 10)

barWidth = 0.35


# create the plot space upon which to plot the data
fig, ax = plt.subplots()

rects1 = ax.bar(x - barWidth/2, dados, barWidth, label='Men')
rects2 = ax.bar(x + barWidth/2, dados, barWidth, label='Women')

# add the x-axis and the y-axis to the plot
ax.bar(metricas, dados, color="green")
#plt.xticks([r + barWidth for r in range (len(dados))],[ "Resultado 1","Resultado 2","Resultado 3","Resultado 4"])
plt.title('Request mais rápido e mais demorado')
plt.xlabel('Medidas de resultado')
plt.ylabel(' Ping (mms)')
plt.legend()

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    #xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(rects1)
autolabel(rects2)

plt.show() 
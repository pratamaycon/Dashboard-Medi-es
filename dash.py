
import csv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

dados = []
with open('dataset.csv', newline='') as f:
    reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE) # ler o arquivo csv
    for row in reader:
        for i in row:
            if i != 'Minimo' and  i !="Media" and i !="Maximo" :
                dados.append(i) # coloca apenas o valores em lista de dados
    f.close()

labels = ['Wikipedia', 'Google', 'Amazon', 'LocalHost']
minimo = [ dados[0], dados[3], dados[6], dados[9] ]
media = [ dados[1], dados[4], dados[7], dados[10] ]
maximo = [ dados[2], dados[5], dados[8], dados[11] ]


x = np.arange(len(labels))  # os locais das etiquetas
width = 0.35  # a largura das barras

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, minimo, width, label='mínimo')
rects2 = ax.bar(x + width/4, media, width, label='média')
rects3 = ax.bar(x + width, maximo, width, label='máximo')


# Adicione um pouco de texto para etiquetas, título e etiquetas personalizadas do eixo x, etc.
ax.set_title('Gráfico de desempenho de cada request e a relação de tempo min, med, max')
ax.set_ylabel('Latência (ms)')
ax.set_xlabel('Número de Requests (Em ordem de Execução)')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

fig.tight_layout()

plt.show()

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


dados = list(map(float, dados)) # converte a lista de strings em lista de números float

labels = ['Localhost', 'Amazon', 'Google', 'Wikipédia']
minino = [dados[9], dados[6], dados[3], dados[0]]
medio = [dados[10], dados[7], dados[4], dados[1]]
maximo = [dados[11], dados[8], dados[5], dados[2]]

ind = np.arange(len(labels))  # os x locais para os grupos
width = 0.35 # a largura das barras

fig, ax = plt.subplots()
rects1 = ax.bar(ind - width/2, minino, width,
                label='Mínimo')
rects2 = ax.bar(ind + width/4, medio, width,
                label='Média')
rects3 = ax.bar(ind + width, maximo, width,
                label='Máximo')


# Adicione um pouco de texto para etiquetas, título e etiquetas personalizadas do eixo x, etc.
ax.set_title('Gráfico de desempenho de cada request e a relação de tempo min, med, max')
ax.set_ylabel('Latência (ms)')
ax.set_xlabel('Número de Requests (Em ordem de Execução)')
ax.set_xticks(ind)
ax.set_xticklabels(labels)
ax.legend()



def autolabel(rects, xpos='center'):
    """
    Anexe um rótulo de texto acima de cada barra em * rects *, exibindo sua altura.
    * xpos * indica qual lado colocar o texto w.r.t. o centro de
    o bar. Pode ser um dos seguintes {'center', 'right', 'left'
    """

    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0, 'right': 1, 'left': -1}

    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos]*3, 3),  # use deslocamento de 3 pontos
                    textcoords="offset points",  # em ambas as direções
                    ha=ha[xpos], va='bottom')


autolabel(rects1)
autolabel(rects2)
autolabel(rects3)


fig.tight_layout()

plt.show()








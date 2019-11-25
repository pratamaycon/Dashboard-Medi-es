import requests #Requests é uma biblioteca HTTP, escrita em Python, para seres humanos. Uso básico dos métodos de GRUD.
import sys # Este módulo fornece acesso a algumas variáveis ​​usadas ou mantidas pelo interpretador.
import time # Este módulo fornece várias funções relacionadas ao tempo


link = "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png" #variavel que vai guardar a url do arquivo a ser baixado
file_name = "downloaded.png" # nome do arquivo
start = time.clock() # Retorna o tempo da CPU ou o tempo real desde o início do processo
response = requests.get(link, stream=True) # resposta
with open(file_name, "wb") as f:
    print("Downloading %s" % file_name)
    response = requests.get(link, stream=True)
    total_length = int(response.headers.get('content-length'))
    print(response.headers["content-type"])
    print(total_length / 1024, "Kb")
    print(int(response.headers["Age"]) * (10 ** -6), "Sec")
    print(response.headers["date"])

    if total_length is None: # no content length header
        f.write(response.content)
    else:
        dl = 0
        for data in response.iter_content(chunk_size=4096):
            dl += len(data)
            f.write(data)
            done = int(50 * dl / total_length)
            print("\r[%s%s] %.2f Kbps" % ('=' * done, ' ' * (50-done), dl//(time.clock() - start)/1000))

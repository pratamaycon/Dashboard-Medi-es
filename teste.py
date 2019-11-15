import socket

def verificaHost(hostname):
 resultado = ""
 try:
  socket.gethostbyname(hostname)
  return 1
 except socket.error:
  resultado = "A solicitação ping não pôde encontrar o host %s. Verifique o nome e tente novamente."%(hostname)
  return resultado


print(verificaHost('google.com'))
print(verificaHost('meupaugrosso.com'))
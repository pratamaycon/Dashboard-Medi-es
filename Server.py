import socket

import os

port = 60000
s = socket.socket()
host = socket.gethostname()
s.bind((host, port))
s.listen(5)

print('Server listening....')

while True:
   conn, addr = s.accept()    
   print('Got connection from', addr)
   data = conn.recv(1024)
   print('Server received', repr(data))

   filename='akki.txt'
   b = os.path.getsize(filename)
   f = open(filename,'rb')
   l = f.read(b)

   while (l):

      conn.send(l)

      l = f.read(b)
   f.close()

   print('Done sending')
   conn.send('Thank you for connecting')
   conn.close()
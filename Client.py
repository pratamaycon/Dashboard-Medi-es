import socket
import time
import os

s = socket.socket()
host = socket.gethostname()
port = 60000

t1 = time.time()
s.connect((host, port))
s.send("Hello server!")

with open('received_file', 'wb') as f:
    print('file opened')
    t2 = time.time()
    while True:

        data = s.recv(1024)

        if not data:
            break

        f.write(data)
        t3 = time.time()

print(data)
print('Total:', t3 - t1)
print('Throughput:', round((1024.0 * 0.001) / (t3 - t1), 3),)
print('K/sec.')
f.close()
print('Successfully received the file')
s.close()
print('connection closed')
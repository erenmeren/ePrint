import socket
from threading import Thread
import logging
import boto3
import time
from botocore.exceptions import ClientError

# socket
TCP_IP = '0.0.0.0'
TCP_PORT = 9100
BUFFER_SIZE = 1024

# aws s3
BUCKET_NAME = 'eprint-test'
FOLDER_NAME = 'bubu-coffee-shop/'

class ClientThread(Thread):

  def __init__(self, ip, port, sc):
    Thread.__init__(self)
    self.ip = ip
    self.port = port
    self.sc = sc
    print(" New thread started for "+ip+":"+str(port))

  def run(self):
    file_name = 'print.pdf'
    f = open(file_name,'wb')
    while True:
      l = sc.recv(1024)
      while (l):
        f.write(l)
        l = sc.recv(1024)
      if not l:
        f.close()
        self.sc.close()
        # send file to aws s3
        upload_file(file_name) 
        break

def upload_file(file_name):
    # Upload the file
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file( file_name, BUCKET_NAME, (FOLDER_NAME+str(time.time()).replace(".", "")+".pdf") )
    except ClientError as e:
        logging.error(e)
        return False
    return True
  


#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s = socket.socket()
s.bind((TCP_IP, TCP_PORT))
threads = []

while True:
  s.listen(10)
  print("Waiting for incoming connections...")
  (sc, (ip, port)) = s.accept()
  print('Got connection from ', (ip, port))
  newthread = ClientThread(ip, port, sc)
  newthread.start()
  threads.append(newthread)

for t in threads:
  t.join()
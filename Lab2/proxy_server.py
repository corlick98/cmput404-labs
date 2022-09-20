#!/usr/bin/env python3
import socket
import time
import sys

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024


#create a tcp socket
def create_tcp_socket():
    print('Creating socket')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print(f'Failed to create socket. Error code: {str(msg[0])} , Error message : {msg[1]}')
        sys.exit()
    print('Socket created successfully')
    return s

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

#send data to server
def send_data(serversocket, payload):
    print("Sending payload")    
    try:
        serversocket.sendall(payload.encode())
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")

def main():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("\nConnected by", addr)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_s:
                try:
                    #define address info, payload, and buffer size
                    host = 'www.google.com'
                    port = 80
                    payload = f'GET / HTTP/1.0\r\nHost: {host}\r\n\r\n'
                    buffer_size = 4096
                    forward = create_tcp_socket()
                    remote_ip = get_remote_ip(host)

                    forward.connect((remote_ip, port))
                    print(f'Socket Connected to {host} on ip {remote_ip}')

                    send_data(forward, payload)
                    forward.shutdown(socket.SHUT_WR)

                    full_data = b""
                    while True:
                        data = forward.recv(buffer_size)
                        if not data:
                            break
                        full_data += data
                    # print(full_data)
                    print("Collected data from forward connection")
                    conn.sendall(full_data)
                    print("Sent data to original client")
                    time.sleep(5)
                    conn.close()

                except Exception as e:
                    print(e)
                finally:
                    proxy_s.close()

if __name__ == "__main__":
    main()

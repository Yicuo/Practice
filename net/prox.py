import sys
import socket
import traceback
import threading


def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host, local_port))
    except:
        traceback.print_exc()
        print("Failed to listen on {0}:{1}".format(local_host, local_port))
        sys.exit(0)

    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port))
        proxy_thread.start()


def main():
    if len(sys.argv[1:]) != 5:
        print("Usage: python prox.py [localhost] [local_port] [remote_host] [remote_port] [receive_first]")
        sys.exit(0)

    localhost = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    receive_first = True if 'True' in sys.argv[5] else False
    server_loop(local_host, local_port, remote_host, remote_port, receive_first)

def proxy_handler(client_socket, remote_host, remote_port):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            print("[==>] Reveived {0} bytes data from localhost.".format(len(local_buffer))
            hexdump(local_buffer)
            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[==>] Send to remote.")

        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print("[<==] Reveived {0} bytes data from remote.".format(len(local_buffer))
            hexdump(remote_buffer)
            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("[==>] Send to localhost.")

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing connections")

            break

def hexdump(src, length=16):
    pass


def receive_from(connection):
    buffer = b''

    connection.settimeout(2)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except:
        pass

    return buffer

def request_handler(buffer):
    #some changes
    return buffer

def response_handler(buffer):
    #some changes
    return buffer

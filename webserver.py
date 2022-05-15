import sys
import time
import socket
import threading
import signal

class WebServer(object):
    def __init__(self, port=8080):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = port
        self.content_dir = 'files'

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            print(f'Server running on {self.host}:{self.port}')
            self.socket.bind((self.host, self.port))
        except Exception as e:
            print(f'ERROR: Could not bind to port {self.port}')
            self.shutdown()
            sys.exit(1)

        self.socket_listen()

    def shutdown(self):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except:
            pass

    def generate_headers(self, response_code):
        header = ''
        if response_code == 200:
            header += 'HTTP/1.1 200 OK\n'
        else:
            header += 'HTTP/1.1 404 Not Found\n'

        time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        header += f'Date: {time_now}\n'
        header += 'Server: Simple-python-Server\n'
        header += 'Connection: close\n\n'
        return header

    def socket_listen(self):
        self.socket.listen(5)
        while True:
            (client, addr) = self.socket.accept()
            client.settimeout(99)
            print(f'Received connection from {client}:{addr}')
            threading.Thread(target=self.handle_client, args=(client, addr)).start()

    def handle_client(self, client, address):
        PACKET_SIZE = 1024
        while True:
            print('Client ', client)
            data = client.recv(PACKET_SIZE).decode()

            if not data: break

            request_method = data.split(' ')[0]
            print('Request: ', data)

            if request_method == 'GET' or request_method == 'HEAD':
                file_requested = data.split(' ')[1]
                file_requested = file_requested.split('?')[0]

                if file_requested == '/':
                    file_requested = '/index.html'

                filepath_to_serve = self.content_dir + file_requested
                print(f'Serving file {filepath_to_serve}')

                try:
                    f = open(filepath_to_serve, 'rb')
                    if request_method == 'GET':
                        response_data = f.read()
                    f.close()
                    response_header = self.generate_headers(200)
                except Exception as e:
                    print('file not found, serving 404')
                    response_header = self.generate_headers(404)

                response = response_header.encode()
                if request_method == 'GET':
                    response += response_data

                client.send(response)
                client.close()
                break
            elif request_method == 'POST':
                pass

            else:
                print(f"Unknown HTTP request method: {request_method}")


def shutdownServer(sig, unused):
    server.shutdown()
    sys.exit(1)

def main():
    signal.signal(signal.SIGINT, shutdownServer)
    server = WebServer(8080)
    server.start()
    print('Press Ctrl+C to shut down server.')

if __name__ == '__main__':
    main()
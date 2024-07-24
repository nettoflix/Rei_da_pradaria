# Classe de base para enviar e receber mensagens UDP
# (salvar esse arquivo como UDPsocket.py)

from socket import *  # Importando o módulo socket

class UDPSocket(socket):
    def __init__(self, host, port, servidor = False):
        super().__init__(AF_INET, SOCK_DGRAM) # SOCK_DGRAM = UDP
        self.host = host
        self.port = port

        if servidor:
            self.bind((host,port))
            self.setblocking(0) # Set non-blocking mode

    def send_message(self, message, host, port):
        self.sendto(message.encode(), (host, port))

    def receive_message(self, buffer_size=1024):
        try:
            data, addr = self.recvfrom(buffer_size)
            return data.decode(), addr
        except BlockingIOError:
        # No data available, continue or perform other tasks
            pass#print("No data available")
            return -1, -1


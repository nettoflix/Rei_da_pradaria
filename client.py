from turtle    import *
from random    import *
from UDPsocket import *

# Executando cliente
t = Turtle()
title("Cliente")    # cria uma tartaruga

# usar "localhost" se servidor for local ou usar o endereço IP do servidor 
cliente = UDPSocket('localhost', 9999) # usando porta 9999

while True:
    t.right(randint(-30,30))   # anda aleatoriamente
    t.forward(1)

    # envia a coordenada da tartaruga para um servidor remoto
    cliente.send_message(str(t.pos()), cliente.host , cliente.port)    
    print(f"Enviou mensagem para {cliente.host}:{cliente.port}")

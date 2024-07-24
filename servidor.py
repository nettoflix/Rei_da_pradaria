from turtle    import *
from UDPsocket import *

# Executando servidor
t = Turtle()
title("Servidor")  # cria uma tartaruga

# endereço "0.0.0.0" significa que o servidor escuta em todas as interfaces de rede
# está usando porta 9999 (importante que seja a mesma do cliente)
servidor = UDPSocket("0.0.0.0", 9999, servidor=True)  

while True:
  message, addr = servidor.receive_message()            
  if(message == -1):
    continue
  print(f"Recebeu mensagem de {addr}: {message}")
  # se recebeu uma coordenada do tipo "(x,y)", faz tartaruga ir pra lá
  if message[0] == "(":
    coord = float(message[1:message.index(",")]), float(message[message.index(",")+1:-2])
    t.goto(coord)

from turtle import *
import random
import math
import time
import gc
from UDPsocket import *
import sys
import ast
import uuid
import json

#####configurações da tela
wn = Screen()
wn.bgcolor("black")
wn.title("Rei da Pradaria")
wn.setup(600,650)
wn.tracer(0)

#lista de dos gifs utilizados
images = ["arbusto.gif", "obstaculo.gif",
          "personagem_baixo.gif", "personagem_cima.gif",
          "personagem_direita.gif", "personagem_esquerda.gif",
          "zumbi.gif", "troll.gif","vida.gif", "walking_down.gif", "walking_left.gif", "walking_up.gif", "walking_right.gif"]

#iteração que registra todos os shapes da lista
for image in images:
    register_shape(image)


#Classe que desenha o mapa
class Pen(Turtle):
    def __init__(self):
        Turtle.__init__(self)
        self.penup()
        self.speed(0)
        self.shapesize(1.6,1.6)
        self.sla = True
        self.xy_enemies = []   #guarda a posição de todos os inimigos_1
        self.xy_enemies_2 = []  #guarda a posição de todos os inimigos_2

    #função que desenha as vidas      
    def draw_lifes(self):
        if player.lifes == 3:
			
            self.goto(-260,300)
            self.shape('vida.gif')
            self.stamp()
            self.goto(-220,300)
            self.stamp()
            self.goto(-180,300)
            self.stamp()
                 




#Classe do player
class Player(Turtle):
    def __init__(self):
        Turtle.__init__(self)
        self.shape("walking_down.gif")
        self.penup()
        self.step = 12 #quantidade de pixels que o player anda
        self.kills = 0 #quantidade de inimigos que o player matou
        self.lifes = 3 #quantidade de vidas que o player inicia
        self.isDead = False
        self.enemyHits = [0] * 24

    #funções que definem para onde o player vai
    def go_up(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor() + self.step

        self.shape(self.personagem_cima)

        if (move_to_x,move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_down(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor() - self.step

        self.shape(self.personagem_baixo)

        if (move_to_x,move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_left(self):
        move_to_x = self.xcor() - self.step
        move_to_y = self.ycor()

        self.shape(self.personagem_esquerda)

        if (move_to_x,move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_right(self):
        move_to_x = self.xcor() + self.step
        move_to_y = self.ycor()

        self.shape(self.personagem_direita)

        if (move_to_x,move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    #função que consefere se o player colidiu com algo
    def is_collision(self, other):
        a = self.xcor()-other.xcor()
        b = self.ycor()-other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))

        if distance < 30:
            return True
        else:
            return False
    def hide(self):
        self.goto(2000,2000)
        self.hideturtle()
    def setRoupas(self, up,down,left,right):
        self.personagem_cima = up
        self.personagem_baixo = down
        self.personagem_esquerda = left
        self.personagem_direita = right
        self.shape(down)
    def moveto(self, pos):
        x, y = pos
        #print("move X: ", x)
        ##print("Y:", y)
        #print("Xcor: ", self.xcor())
        if(x > self.xcor()):
            self.shape("walking_right.gif")
        elif(x < self.xcor()):
            self.shape(self.personagem_esquerda)
        elif(y > self.ycor()):
            self.shape(self.personagem_cima)
        elif(y < self.ycor()):
            self.shape(self.personagem_baixo)
        self.goto(pos)
    def resetHits(self):
        self.enemyHits = [0] * 24
    
#classe da bala
class Bullet(Turtle):
    def __init__(self):
        Turtle.__init__(self)
        self.penup()
        self.color('gray')
        #define onde a bala ira nascer
        self.x = player.xcor()
        self.y = player.xcor()
        self.move = None
        #coloca a bala fora da tela no inicio do jogo
        self.setx(1000)
        self.sety(1000)
        self.shape("square")
        self.shapesize(stretch_wid=0.3,stretch_len=0.3,outline=None)
        #define se a bala esta pronta pra ser atirada
        self.status = "ready"
        #define se existe colisão
        self.colisao = 'nao'
        self.goingto = None
        self.uuid = uuid.uuid4()

    #funções que controla para onde a bala deve ir
    def shoot_right(self):
        if self.status == "ready":
            self.status = "SLA"
            self.move_right()
    def move_right(self):
        if self.move != 'right':
            self.goto(player.xcor(),player.ycor())
        
        self.showturtle()
        self.move = 'right'
        self.shoot(self.move)

    def shoot_left(self):
        if self.status == "ready":
            self.status = "SLA"
            self.move_left()

    def move_left(self):
        if self.move != 'left':
            self.goto(player.xcor(),player.ycor())
        self.showturtle()
        self.move = 'left'
        self.shoot(self.move)
    def move_up(self):
        if self.move != 'up':
            self.goto(player.xcor(),player.ycor())
        self.showturtle()
        self.move = 'up'
        self.shoot(self.move)  
    def move_down(self):
        if self.move != 'down':
            self.goto(player.xcor(),player.ycor())
        self.showturtle()
        self.move = 'down'
        self.shoot(self.move)  
    def shoot_up(self):
        if self.status == "ready":
            self.status = "SLA"
            self.move_up()

    def shoot_down(self):
        if self.status == "ready":
            self.status = "SLA"
            self.move_down()

    #função que move a bala pra direção selecionada nas funções acima
    def shoot(self,move):
        if self.move == 'left':
            move_to_x = self.xcor() - 1
            move_to_y = self.ycor()
        if self.move == 'right':
            move_to_x = self.xcor() + 1
            move_to_y = self.ycor()
        if self.move == 'up':
            move_to_x = self.xcor() 
            move_to_y = self.ycor() + 1
        if self.move == 'down':
            move_to_x = self.xcor() 
            move_to_y = self.ycor() - 1
            

        # if move_to_x > 224 or move_to_x < -224:
        #     #self.hideturtle()
        #     #self.goto(player.xcor(),player.ycor())
        #     self.status = "ready"
        #     self.move = "sla"
        #     return
            
        # if move_to_y > 224 or move_to_y < -224:
        #     #self.hideturtle() 
        #     #self.goto(player.xcor(),player.ycor())
        #     self.status = "ready"
        #     self.move = "sla"
        #     return   
        
        #se a colisao existe tira a bala da tela e deixa voce atirar de novo
        # if self.colisao == 'sim':
        #     #self.hideturtle() 
        #     #self.goto(player.xcor(),player.ycor())
        #     self.status = "ready"
        #     self.move = "sla"
        #     self.colisao = 'nao'
        #     return 
            
        #chama a mesma função de antes para mover a bala continuamente a cada 3 milisegundos
        self.goto(move_to_x, move_to_y)
        if self.move == 'left':
            ontimer(self.move_left,t=3)
        if self.move == 'right':
            ontimer(self.move_right,t=3)
        if self.move == 'up':
            ontimer(self.move_up,t=3)
        if self.move == 'down':
            ontimer(self.move_down,t=3)
	   
	#função que define se tem colisao
    def is_collision(self, other):
        a = self.xcor()-other.xcor()
        b = self.ycor()-other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))

        if distance < 20:
            self.colisao = 'sim'
            # enemy_2.life -= 1
            return True
        else:
            return False
    def destroy(self):
        self.clear()
        self.penup()
        self.goto(2000,2000)
        self.hideturtle()
        #turtle_list.remove(self)
           # a seguir é pra evitar memory leaks
        # Remove qualquer outra referencia a esse turtle
        del self

		   
	     
         
        
#classe do inimigo 1        
class Enemy(Turtle):
    def __init__(self, x, y):
        Turtle.__init__(self)
        self.shape("zumbi.gif")
        self.status = 'vivo'
        self.penup()
        self.speed = 32 #define a velocidade do inimigo
        self.goto(x,y)
        self.colis = False #define se tem colisao
        
    #definição que move o inimigo
    def move(self):
        self.direction = None
        self.status = 'vivo'
        #sorteia numeros de 1 a 4 que definem para que lado o inimigo vai
        self.direction = random.randint(1,4)
        if self.direction == 1:
            dx,dy = 32,0
        if self.direction == 2:
            dx,dy = -32,0
        if self.direction == 3:
            dx,dy = 0,32
        if self.direction == 4:
            dx,dy = 0,-32
        move_to_x = self.xcor() + dx
        move_to_y = self.ycor() + dy
        if (move_to_x,move_to_y) not in walls:
            if (move_to_x,move_to_y) not in pen.xy_enemies:
                if self.status == 'vivo':
                    self.goto(move_to_x, move_to_y)
        ontimer(self.move,t=300)

    #função que "destroi" o inimigo
    def destroy(self):
        self.goto(2000,2000)
        self.hideturtle()
        self.status = 'morto' #quando morto o inimigo nao se mexe
        #player.kills += 1

#classe do inimigo 2        
class Enemy_2(Turtle):
    def __init__(self, x, y):
        Turtle.__init__(self)
        self.shape("troll.gif")
        self.penup()
        self.speed(0)
        self.goto(x,y)
        self.life = 2
        self.speed = 32
        self.status = 'vivo'
        who = random.randint(1,2)
        global isOnline
        global player2
        print("isOnline:",isOnline)
        if(isOnline):
            if(who == 1):
                self.chosenPlayer = player
            else:
                self.chosenPlayer = player2
        else:
            self.chosenPlayer = player
        

    def move(self):
        self.direction = None
        if self.chosenPlayer.isDead and self.chosenPlayer == player2:
            self.chosenPlayer = player
        if self.chosenPlayer == player:
            pass#print("player1 lives: ",self.chosenPlayer.lifes)
        else:
            pass#print("player2 lives: ",self.chosenPlayer.lifes)
        #print("chosen lifes: ",self.chosenPlayer.lifes)
        px = self.xcor() - self.chosenPlayer.xcor()
        py =  self.ycor() - self.chosenPlayer.ycor()
        
        
        #o movimento desse inimigo pega com base da posição do player para segui-lo
        if (abs(px) > abs(py)):
            if px > 0:
                self.direction = "left"
            elif px < 0:
                self.direction = "right"
        else:
            if py > 0:
                self.direction = "down"
            elif py < 0:
                self.direction = "up"
        
        dx, dy = 0, 0
        if self.direction == "up":
            dx = 0
            dy = self.speed
        elif self.direction == "down":
            dx = 0
            dy = -self.speed
        elif self.direction == "right":
            dx = +self.speed
            dy = 0
        elif self.direction == "left":
            dx = -self.speed
            dy = 0
        elif self.direction == "nada":
            dx = 0
            dy = 0

        move_to_x = self.xcor() + dx
        move_to_y = self.ycor() + dy
        if (move_to_x,move_to_y) not in walls:
            if (self.xcor(),self.ycor()) not in pen.xy_enemies:
                if self.status == 'vivo':
                    self.goto(move_to_x, move_to_y)
            

            
        
        ontimer(self.move,t=400)

    def destroy(self):
        self.goto(2000,2000)
        self.hideturtle()
        self.status = 'morto'
        #player.kills += 1      
  
##Inicia a comunicação udp
client_port = 9998
servidor_port=9999
isOnline = False
isPlayer1 = True
if len(sys.argv) > 1:
    isOnline = True
    for i, arg in enumerate(sys.argv[1:], start=1):
        print(f"Argument {i}: {arg}")
        if(i == 1):
            client_port = int(arg)
        if(i==2):
            servidor_port = int(arg)
        if(i==3):
            isPlayer1 = int(arg)
            if(isPlayer1 == 1):
                isPlayer1 = True
            else:
                isPlayer1 = False
            print(isPlayer1)

else:
    print("No arguments provided.")
servidor = UDPSocket("0.0.0.0", servidor_port, servidor=True)  
# usar "localhost" se servidor for local ou usar o endereço IP do servidor 
cliente = UDPSocket('localhost', client_port) # usando porta 9999


##Contador de tempo da bala, pra nao poder atirar muito rapido
bulletTimeCount = 0
#cria uma lista de niveis
levels = [""]

       #0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
level_1_1 =[[1,1,1,1,1,1,1,0,0,0, 1, 1, 1, 1, 1, 1],#0wa
          [1,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#1
          [1,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#2
          [1,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#3
          [1,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#4
          [1,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#5
          [1,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#6
          [0,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 0],#7
          [0,0,0,0,0,0,0,0,2,0, 0, 0, 0, 0, 0, 4],#8
          [0,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 0],#9
          [1,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#10
          [1,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#11
          [1,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#12
          [1,0,0,4,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#13
          [1,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#14
          [1,1,1,1,1,1,1,0,4,0, 1, 1, 1, 1, 1, 1]]#15

       #0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
level_1_2 =[[1,1,1,1,1,1,1,0,4, 0, 1, 1, 1, 1, 1, 1],#0wa
          [1,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#1
          [1,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#2
          [1,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#3
          [1,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#4
          [1,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#5
          [1,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#6
          [0,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 0],#7
          [0,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 4],#8
          [4,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 0],#9
          [1,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#10
          [1,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#11
          [1,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#12
          [1,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#13
          [1,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#14
          [1,1,1,1,1,1,1,0,4,0, 1, 1, 1, 1, 1, 1]]#15
          
       #0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
level_2 =[[1,1,1,1,1,1,1,0,0,0, 1, 1, 1, 1, 1, 1],#0
          [1,1,1,1,0,0,0,0,0,0, 0, 0, 0, 1, 1, 1],#1
          [1,1,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 1, 1],#2
          [1,1,0,0,0,0,5,0,0,0, 0, 0, 0, 0, 0, 1],#3
          [1,0,0,0,0,0,0,0,0,0, 0, 0, 5, 0, 0, 1],#4
          [1,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#5
          [1,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#6
          [0,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 0],#7
          [0,0,0,0,0,0,0,0,2,0, 0, 0, 5, 0, 0, 0],#8
          [0,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 0],#9
          [1,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#10
          [1,0,0,0,5,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#11
          [1,0,0,0,0,0,0,0,0,0, 0, 0, 5, 0, 0, 1],#12
          [1,1,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 1, 1],#13
          [1,1,1,1,0,0,0,0,0,0, 0, 0, 0, 1, 1, 1],#14
          [1,1,1,1,1,1,1,0,0,0, 1, 1, 1, 1, 1, 1]]#15
# level_2 =[[1,1,1,1,1,1,1,0,0,0, 1, 1, 1, 1, 1, 1],#0
#           [1,1,1,1,0,0,0,0,0,0, 0, 0, 0, 1, 1, 1],#1
#           [1,1,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 1, 1],#2
#           [1,1,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#3
#           [1,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#4
#           [1,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#5
#           [1,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#6
#           [0,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 0],#7
#           [0,0,0,0,0,0,0,0,2,0, 0, 0, 0, 5, 0, 0],#8
#           [0,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 0],#9
#           [1,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#10
#           [1,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#11
#           [1,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#12
#           [1,1,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 1, 1],#13
#           [1,1,1,1,0,0,0,0,0,0, 0, 0, 0, 1, 1, 1],#14
#           [1,1,1,1,1,1,1,0,0,0, 1, 1, 1, 1, 1, 1]]#15

#inclui as matrizes na lista
levels.append(level_1_1)
levels.append(level_1_2)
levels.append(level_2)


#menu principal
def menu():
    pen.hideturtle()
    wn.bgpic("menu.png")


#cria o mapa    
def setup_maze(level):
    
    wn.bgpic("level1.png")
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]
            #define o tamanho da tela
            screen_x = -240 + (x*32)
            screen_y = 240 - (y*32)

            #define a posição de cada coisa no mapa, alem de colocar a posição dos obstaculos na lista de obstaculos para colisão
            if character == 1:
                pen.shape("arbusto.gif")
                pen.goto(screen_x, screen_y)
                walls.append((screen_x,screen_y))
            if character == 0:
                pen.goto(screen_x, screen_y)
                chao.append((screen_x, screen_y))
            if character == 2:
                player.goto(screen_x, screen_y)
            if character == 3:
                pen.shape("obstaculo.gif")
                pen.goto(screen_x, screen_y)
                walls.append((screen_x,screen_y))
            if character == 4:
                pen.goto(screen_x, screen_y)
                enemies.append(Enemy(screen_x, screen_y))
            if character == 5:
                pen.goto(screen_x, screen_y)
                enemies_2.append(Enemy_2(screen_x, screen_y))

#definição que começa o jogo
def play():
    global isOnline
    global players_kills
    global targetChanged
    if pen.sla == True:         #se o jogo nao foi iniciado ainda a função é chamada, senao nao
        pen.sla = False
        setup_maze(levels[1]) #inicia o primeiro nivel
        pen.draw_lifes() #chama a função que desenha vidas
        if(isPlayer1):
            for enemy_2 in enemies_2:
                ontimer(enemy_2.move, t=300) #faz o inimigo andar
            for enemy in enemies:
                ontimer(enemy.move, t=300) #faz o inimigo andar
            
        while True:
            if(isOnline):
                global player2Pos
                global enemyPositions_received
                ##criar o dicinario de dados para enviar na mensagem
                dados = {}
                dados["Player2Pos"] = player.pos()
                dados["EnemyPositions"] = pen.xy_enemies
                dados["Enemy2Positions"] = pen.xy_enemies_2
                bullets_directions = [bullet.goingto for bullet in bullets]
                bullets_positions = [bullet.pos() for bullet in bullets]
                bullets_uuid = [str(bullet.uuid) for bullet in bullets]
                dados["bullets_directions"] = bullets_directions
                dados["bullets_positions"] = bullets_positions
                dados["bullets_uuid"] = bullets_uuid
                dados["players_kills"] = players_kills
                dados["player2lifes"] = player.lifes
                dados["Player2_enemyhits"] = player.enemyHits
                player.resetHits()
               # print("dados", dados)
                #print('\n')
                    
                #print(dados)
                cliente.send_message(json.dumps(dados), cliente.host , cliente.port)    #envia a posição do player1 para o player2
                message, addr = servidor.receive_message()            
                #print(message)
                if(message != -1):
                    global isPlayer2Connected
                    isPlayer2Connected = True
                    #print(f"Recebeu mensagem de {addr}: {message}")
                    # se recebeu uma coordenada do tipo "(x,y)"
                    # if message[0] == "(":
                    #     coord = float(message[1:message.index(",")]), float(message[message.index(",")+1:-2])
                    #     player2.showturtle()
                    #     player2.goto(coord)
                   # print("MEssage:", message)
                    #message_dic = ast.literal_eval(message)
                   # message_str = json.dumps(message)
                    message_dic = json.loads(message)
                    #print(message_dic)
                    player2Pos = message_dic['Player2Pos']
                    player2.showturtle()
                    ##player2.goto(player2Pos)
                    player2.moveto(player2Pos)
                    if(not isPlayer1):
                        #print("Received enemy positions", enemyPositions_received)
                        enemyPositions_received = message_dic['EnemyPositions']
                        enemy2Positions_received = message_dic['Enemy2Positions']
                        for i in range(len(enemyPositions_received)):
                            if(len(enemies) == len(enemyPositions_received)):
                                #print("Enemy pos receivid",enemyPositions_received)
                                enemies[i].goto(enemyPositions_received[i])
                        for i in range(len(enemy2Positions_received)):
                            if(len(enemies_2) == len(enemy2Positions_received)):
                                #print("Enemy pos receivid",enemyPositions_received)
                                enemies_2[i].goto(enemy2Positions_received[i])

                    player2BulletsPos = message_dic['bullets_positions']
                    player2BulletsDir = message_dic['bullets_directions']  
                    bullets_uuid = [uuid.UUID(uid) for uid in message_dic['bullets_uuid']]
                    if(int(message_dic['players_kills']) > players_kills):
                        players_kills = int(message_dic['players_kills'])
                    player2.lifes = message_dic['player2lifes']
                    player2.enemyHits = message_dic['Player2_enemyhits']
                    #print(message_dic)  
                    # print("bullets_uuid", bullets_uuid)
                    for i in range(len(player2BulletsDir)):
                        uuids_registereded = [bullet.uuid for bullet in bullets2]
                        if(bullets_uuid[i] not in uuids_registereded):
                            newBullet = None
                            if(player2BulletsDir[i] == 'right'):
                                print("createBulletRightForPlayer2")
                                newBullet = createBulletRightForPlayer2(player2BulletsPos[i])
                                newBullet.goto(player2.pos())
                            if(player2BulletsDir[i] == 'left'):
                                newBullet = createBulletLeftForPlayer2(player2BulletsPos[i])
                                newBullet.goto(player2.pos())
                            if(player2BulletsDir[i] == 'up'):
                                newBullet = createBulletUpForPlayer2(player2BulletsPos[i])
                                newBullet.goto(player2.pos())
                            if(player2BulletsDir[i] == 'down'):
                                newBullet = createBulletDownForPlayer2(player2BulletsPos[i])
                                newBullet.goto(player2.pos())
                            if(newBullet != None):
                                newBullet.uuid = bullets_uuid[i]
            
                if(not isPlayer1 and not targetChanged):
                        if(player2.isDead):
                            print("other is dead")
                            for enemy_2 in enemies_2:
                                ontimer(enemy_2.move, t=300)
                            targetChanged = True    

            if(player.lifes <= 0): return
            #vamos supor que a gente recebe a poisção do player2 via lan 
            #também recebemos a quantidade de balas desse player2 e a posição de cada uma
            #atualizamos a posição do player2 e das balas dele
            #checamos se o inimigo foi atingido por alguma bala do player2 ou se o player2 morreu


            global bulletTimeCount
            bulletTimeCount = bulletTimeCount + 1
            n_enemies_1_1 = 3   #numero de inimigos mortos necessarios para nova onda de inimigos aparecer
            n_enemies_1_2 = 8   #numero de inimigos mortos necessarios para ir para segunda fase
            n_enemies_2 = 13    #numero de inimigos necessarios para ganhar o jogo
            #print("1- Enemies size:", len(enemies))
            #print("PLayer Kills:", players_kills)
            if(isOnline):
                for i in range(len(player2.enemyHits)):
                    if(len(enemies)> i):
                        if(i<3):
                            if(player2.enemyHits[i] == 1):
                                enemies[i].destroy()
                                player2.enemyHits[i] = 0
                        if(i >=3 and i<8):
                            if(player2.enemyHits[i] == 1):
                                enemies[i].destroy()
                                player2.enemyHits[i] = 0
                    if(len(enemies_2) >= (i-8)):
                        print("enemyhits", player2.enemyHits)
                        if(player2.enemyHits[i] == 1):
                            enemies_2[i-8].life -= 1
                            player2.enemyHits[i-8] = 0
                            if(enemies_2[i-8].life <= 0):
                                enemies_2[i-8].destroy() 
                if(player2.lifes <=0 ):
                    player2.isDead = True

            if players_kills == (n_enemies_1_1): #se a quantidade necessaria de inimigos forem mortos ele spawna mais inimigos
                players_kills += 1
                setup_maze(levels[2])
                print("spawna mais", len(enemies))
                #Turtle.bye()
                for i in range(len(enemies)):
                    if(isPlayer1):
                        ontimer(enemies[i].move, t=300)
                    else:
                        if(len(enemyPositions_received) > 0):
                            pass#enemies[i].goto(enemyPositions_received[i])
                        #enemy.goto(enemyPositions_received.pop(0))
            if players_kills == (n_enemies_1_2): #se todos os inimigos da fase 1 forem mortos passa pra fase 2
                print("passa pra fase 2")
                players_kills += 1
                pen.write('level 2')
                enemy.showturtle()
                setup_maze(levels[3])
                wn.bgpic('level2.png')
                for i in range(len(enemies_2)):
                    if(isPlayer1):
                        ontimer(enemies_2[i].move, t=300)
                    else:
                        pass#enemies_2[i].goto(enemy2Positions_received[i])


                
            if players_kills == (n_enemies_2): #se todos os inimigos da fase 2 forem mortos acaba o jogo
                resetscreen()
                wn.bgcolor('black')
                wn.bgpic('fim.png')
                return
            pen.xy_enemies = []
            pen.xy_enemies_2 = []
            for i in range(len(enemies)):
                enemy = enemies[i]
                pen.xy_enemies.append(((enemy.xcor()),(enemy.ycor()))) #inclui a localização de cada inimigo na lista
                for bullet in bullets:
                    if bullet.is_collision(enemy):#"mata" o inimigo se a bala colidir nele
                        enemy.destroy()
                        bullet.destroy()
                        bullets.remove(bullet)
                        players_kills += 1
                        player.enemyHits[i] += 1
                        #print("Length before:", len(bullets))
                       # 
                        #print("Length after:", len(bullets))

                if player.is_collision(enemy): #diminiu uma vida do player se ele colidir com o inimigo
                    print("colison enemy")
                    player.lifes -= 1
                    player.goto(random.choice(chao))#teleporta o inimigo para uma cordenada sem inimigos
                    if player.lifes == 2:
                        pen.goto(-180,300)
                        pen.shape('square')
                        pen.color('black')
                        pen.stamp()
                    if player.lifes == 1:
                        pen.goto(-260,300)
                        pen.color('black')
                        pen.stamp()
                    if player.lifes == 0:
                        pen.clearstamps()
                        resetscreen()
                        wn.bgcolor('black')
                        wn.bgpic('morte.png')
                        return
            for i in range(len(enemies_2)):
                enemy_2 = enemies_2[i]
                #print("enemy_2 life:", enemy_2.life)
                pen.xy_enemies_2.append(((enemy_2.xcor()),(enemy_2.ycor())))
                for bullet in bullets:
                    if bullet.is_collision(enemy_2):
                        enemy_2.life -= 1
                        player.enemyHits[8+i] += 1
                        if enemy_2.life == 0:
                            enemy_2.destroy()
                            bullet.destroy()
                            bullets.remove(bullet)
                            players_kills += 1


                if player.is_collision(enemy_2):
                    if(isPlayer1):
                        player.lifes -= 1
                    player.goto(random.choice(chao))
                    if player.lifes == 2:
                        pen.goto(-180,300)
                        pen.shape('square')
                        pen.color('black')
                        pen.stamp()
                    if player.lifes == 1:
                        pen.goto(-260,300)
                        pen.color('black')
                        pen.stamp()
                    if player.lifes == 0:
                        pen.clearstamps()
                        resetscreen()
                        wn.bgcolor('black')
                        wn.bgpic('morte.png')
                #Bullets que devem ser removidas
            to_remove = [bullet for bullet in bullets if bullet.colisao == 'sim' or bullet.xcor() > 224 or bullet.xcor() < -224 or bullet.ycor() > 224 or bullet.ycor() < -224]

            # Remove as bullets que devem ser removidas
            for bullet in to_remove:
                bullets.remove(bullet)
                bullet.destroy()
                gc.collect()
            to_remove = [bullet2 for bullet2 in bullets2 if bullet2.colisao == 'sim' or bullet2.xcor() > 224 or bullet2.xcor() < -224 or bullet2.ycor() > 224 or bullet2.ycor() < -224]
            
            for bullet2 in to_remove:
                bullets2.remove(bullet2)
                bullet2.destroy()
                gc.collect()
            wn.update()
bullets = []
bullets2 = []
players_kills = 0
def createBulletRight():
    global bulletTimeCount
    if(bulletTimeCount>700):
        bullet = Bullet()
        bullets.append(bullet)
        bullet.shoot_right()
        bulletTimeCount= 0
        bullet.goingto = 'right'
def createBulletLeft():
    global bulletTimeCount
    if(bulletTimeCount>700):
        bullet = Bullet()
        bullets.append(bullet)
        bullet.shoot_left()
        bulletTimeCount= 0
        bullet.goingto = 'left'
def createBulletUp():
    global bulletTimeCount
    if(bulletTimeCount>700):
        bullet = Bullet()
        bullets.append(bullet)
        bullet.shoot_up()
        bulletTimeCount= 0
        bullet.goingto = 'up'
def createBulletDown():
    global bulletTimeCount
    if(bulletTimeCount>700):
        bullet = Bullet()
        bullets.append(bullet)
        bullet.shoot_down()
        bulletTimeCount= 0
        bullet.goingto = 'down'
def createBulletDownForPlayer2(pos):
    bullet2 = Bullet()
    bullet2.goto(pos)
    bullets2.append(bullet2)
    bullet2.shoot_down()
    return bullet2
def createBulletUpForPlayer2(pos):
    bullet2 = Bullet()
    bullet2.goto(pos)
    bullets2.append(bullet2)
    bullet2.shoot_up()
    return bullet2
def createBulletLeftForPlayer2(pos):
    bullet2 = Bullet()
    bullet2.goto(pos)
    bullets2.append(bullet2)
    bullet2.shoot_left()
    return bullet2
def createBulletRightForPlayer2(pos):
    bullet2 = Bullet()
    bullet2.goto(pos)
    bullets2.append(bullet2)
    bullet2.shoot_right()
    return bullet2
def killEnemies():
    global players_kills
    global player
    for i in range(len(enemies)):
        enemy = enemies[i]
        if(enemy.status == 'vivo'):
            pen.xy_enemies.append(((enemy.xcor()),(enemy.ycor())))
            enemy.destroy()
            players_kills += 1
            player.enemyHits[i] += 1



pen = Pen() 
player = Player()
player.setRoupas("personagem_cima.gif","personagem_baixo.gif","personagem_esquerda.gif","personagem_direita.gif")

player2 = Player()
player2.setRoupas("walking_up.gif","walking_down.gif","walking_left.gif","walking_right.gif")
enemy2Positions_received = []
player2.hide()
player2Pos = (2000,2000)
isPlayer2Connected = False
enemyPositions_received = []

#playerHits = [0] * 24
#player2Hits = [0] * 24
#bullet = Bullet()
targetChanged = False
enemies = []
enemies_2 = []
#define paredes para colisão
walls = [(-272,-48),(-272,-16),(-272,16),(272,-48),(272,-16),(272,16),(48,272),(16,272),(-16,272),(48,-272),(16,-272),(-16,-272)]
chao = []
menu()

listen()
onkey(player.go_left,"a")
onkey(player.go_right,"d")
onkey(player.go_up,"w")
onkey(player.go_down,"s")

onkey(createBulletRight, "Right")
onkey(createBulletLeft, "Left")
onkey(createBulletUp, "Up")
onkey(createBulletDown, "Down")
onkey(killEnemies, "k")
onkey(play,"p")
onkey(bye,"q")


wn.mainloop()



    
  

                
            

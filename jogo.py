from turtle import *
import random
import math
import time
import gc

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
          "zumbi.gif", "troll.gif","vida.gif"]

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
        self.shape("personagem_baixo.gif")
        self.penup()
        self.step = 12 #quantidade de pixels que o player anda
        self.kills = 0 #quantidade de inimigos que o player matou
        self.lifes = 3 #quantidade de vidas que o player inicia

    #funções que definem para onde o player vai
    def go_up(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor() + self.step

        self.shape("personagem_cima.gif")

        if (move_to_x,move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_down(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor() - self.step

        self.shape("personagem_baixo.gif")

        if (move_to_x,move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_left(self):
        move_to_x = self.xcor() - self.step
        move_to_y = self.ycor()

        self.shape("personagem_esquerda.gif")

        if (move_to_x,move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_right(self):
        move_to_x = self.xcor() + self.step
        move_to_y = self.ycor()

        self.shape("personagem_direita.gif")

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
        player.kills += 1

#classe do inimigo 2        
class Enemy_2(Turtle):
    def __init__(self, x, y):
        Turtle.__init__(self)
        self.shape("troll.gif")
        self.penup()
        self.speed(0)
        self.goto(x,y)
        self.life = 12
        self.speed = 32
        self.status = 'vivo'
        

    def move(self):
        self.direction = None
        px = self.xcor() - player.xcor()
        py =  self.ycor() - player.ycor()
        
        
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
        player.kills += 1      
  

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
          [0,0,0,0,0,0,0,0,2,0, 0, 0, 0, 0, 0, 0],#8
          [0,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 0],#9
          [1,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#10
          [1,0,0,0,5,0,0,0,0,0, 0, 0, 0, 0, 0, 1],#11
          [1,0,0,0,0,0,0,0,0,0, 0, 0, 5, 0, 0, 1],#12
          [1,1,0,0,0,0,0,0,0,0, 0, 0, 0, 0, 1, 1],#13
          [1,1,1,1,0,0,0,0,0,0, 0, 0, 0, 1, 1, 1],#14
          [1,1,1,1,1,1,1,0,0,0, 1, 1, 1, 1, 1, 1]]#15

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
    if pen.sla == True:         #se o jogo nao foi iniciado ainda a função é chamada, senao nao
        pen.sla = False
        setup_maze(levels[1]) #inicia o primeiro nivel
        pen.draw_lifes() #chama a função que desenha vidas
        for enemy_2 in enemies_2:
            
           ontimer(enemy_2.move, t=300) #faz o inimigo andar
        for enemy in enemies:
            
            ontimer(enemy.move, t=300) #faz o inimigo andar
        while True:
            global bulletTimeCount
            bulletTimeCount = bulletTimeCount + 1
            n_enemies_1_1 = 3   #numero de inimigos mortos necessarios para nova onda de inimigos aparecer
            n_enemies_1_2 = 8   #numero de inimigos mortos necessarios para ir para segunda fase
            n_enemies_2 = 13    #numero de inimigos necessarios para ganhar o jogo
            if player.kills == (n_enemies_1_1): #se a quantidade necessaria de inimigos forem mortos ele spawna mais inimigos
                player.kills += 1
                setup_maze(levels[2])
                for enemy in enemies:
                    ontimer(enemy.move, t=300)
            
            if player.kills == (n_enemies_1_2): #se todos os inimigos da fase 1 forem mortos passa pra fase 2
                player.kills += 1
                pen.write('level 2')
                enemy.showturtle()
                setup_maze(levels[3])
                wn.bgpic('level2.png')
                for enemy_2 in enemies_2:
                    ontimer(enemy_2.move, t=300)
                
            if player.kills == (n_enemies_2): #se todos os inimigos da fase 2 forem mortos acaba o jogo
                resetscreen()
                wn.bgcolor('black')
                wn.bgpic('fim.png')
                return
            pen.xy_enemies = []
            pen.xy_enemies_2 = []
            for enemy in enemies:
                for bullet in bullets:
                    pen.xy_enemies.append(((enemy.xcor()),(enemy.ycor()))) #inclui a localização de cada inimigo na lista
                    if bullet.is_collision(enemy):#"mata" o inimigo se a bala colidir nele
                        enemy.destroy()
                        bullet.destroy()
                        print("Length before:", len(bullets))
                       # bullets.remove(bullet)
                        print("Length after:", len(bullets))
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
            for enemy_2 in enemies_2:
                pen.xy_enemies_2.append(((enemy_2.xcor()),(enemy_2.ycor())))
                for bullet in bullets:
                    if bullet.is_collision(enemy_2):
                        enemy_2.life -= 1
                        if enemy_2.life == 0:
                            enemy_2.destroy()
                if player.is_collision(enemy_2):
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
                        return
                #Bullets que devem ser removidas
            to_remove = [bullet for bullet in bullets if bullet.colisao == 'sim' or bullet.xcor() > 224 or bullet.xcor() < -224 or bullet.ycor() > 224 or bullet.ycor() < -224]

            # Remove as bullets que devem ser removidas
            for bullet in to_remove:
                bullets.remove(bullet)
                bullet.destroy()
                gc.collect()
            wn.update()
bullets = []
def createBulletRight():
    global bulletTimeCount
    if(bulletTimeCount>700):
        bullet = Bullet()
        bullets.append(bullet)
        bullet.shoot_right()
        bulletTimeCount= 0
def createBulletLeft():
    global bulletTimeCount
    if(bulletTimeCount>700):
        bullet = Bullet()
        bullets.append(bullet)
        bullet.shoot_left()
        bulletTimeCount= 0
def createBulletUp():
    global bulletTimeCount
    if(bulletTimeCount>700):
        bullet = Bullet()
        bullets.append(bullet)
        bullet.shoot_up()
        bulletTimeCount= 0
def createBulletDown():
    global bulletTimeCount
    if(bulletTimeCount>700):
        bullet = Bullet()
        bullets.append(bullet)
        bullet.shoot_down()
        bulletTimeCount= 0

pen = Pen() 
player = Player()
#bullet = Bullet()

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
onkey(play,"p")
onkey(bye,"q")


wn.mainloop()



    
  

                
            

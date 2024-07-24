from jogo import *
#Classe do player
class Player2(Turtle):
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
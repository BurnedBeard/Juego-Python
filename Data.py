import pygame
import pickle
import random
import math

WIDTH = 1370
HEIGHT = 690
BLACK = (0,0,0)
WHITE = (255,255,255)

HS = 0
def ActHS():
    global HS
    try:
        with open("Archivo","rb") as a:
            HS = pickle.load(a)
    except EOFError:
        with open("Archivo","wb") as a:
            pickle.dump(0, a)
    H = HS
    return H
HS = ActHS()
imagen = 0

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

SCORE = 0

#Sonidos
Sonidos = {
    "romper" : pygame.mixer.Sound("Sonidos/Choque.mp3"),
    "golpe" : pygame.mixer.Sound("Sonidos/Damage.mp3"),
    "bonus" : pygame.mixer.Sound("Sonidos/Bonus.mp3"),
    "bolas" : pygame.mixer.Sound("Sonidos/Fuego.mp3"),
    "boss" : pygame.mixer.Sound("Sonidos/Entrada.mp3"),
    "bDerrota" : pygame.mixer.Sound("Sonidos/Fuegos.mp3"),
    "bDisparo" : pygame.mixer.Sound("Sonidos/Disparo.mp3"),
    "bMiniom" : pygame.mixer.Sound("Sonidos/Laser2.mp3")
}

#Imagenes
Ividas = pygame.image.load("Assets/Vida.png")
Ividas.set_colorkey(WHITE)
iPower2 = pygame.image.load("Assets/power2.png")
iPower2.set_colorkey(WHITE)
iPower3 = pygame.image.load("Assets/power3.png")
iPower3.set_colorkey(WHITE)


class Cartel():
    def __init__(self, txt, f, x,y, central = False) -> None:
        self.texto = txt
        self.font = pygame.font.Font('freesansbold.ttf', f)
        self.x = x
        self.y = y
        self.central = central
        pass

    def draw(self):
        cartel = self.font.render(self.texto, True, WHITE)
        rect = cartel.get_rect()
        rect.x = self.x
        rect.y = self.y
        if self.central:
            rect.center = (self.x, self.y)
        screen.blit(cartel, rect)

class Boton():
    def __init__(self, t, x,y):
        self.Tipo = t
        self.rect1 = pygame.Rect(0,0, 200, 100)
        self.rect1.center = (x,y)
        self.col1 = WHITE
        self.rect2 = pygame.Rect(0,0, self.rect1.width-10,self.rect1.height-10)
        self.rect2.center = (x,y)
        self.col2 = BLACK

        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.text = t       

        self.Press = False
        pass

    def Actualizar(self,screen):
        self.draw(screen)
        self.mouse()

    def mouse(self):
        M = pygame.mouse.get_pos()
        if self.rect1.collidepoint(M[0], M[1]):
            self.col1 = (0,255,0)
            press = pygame.mouse.get_pressed()
            self.Press = press[0]
        else:
            self.col1 = WHITE
            self.Press = False
    
    def draw(self,screen):
        pygame.draw.rect(screen, self.col1, self.rect1)
        pygame.draw.rect(screen, self.col2, self.rect2)
        ley = self.font.render(self.text, True, WHITE)
        rect = ley.get_rect()
        rect.center = self.rect1.center
        screen.blit(ley, rect)

class Tablero():
    def Guardar(array):
        
        t = 0
        with open("Archivo", "rb") as a:
            t = pickle.load(a)
        if t<array:
            with open("Archivo", "wb") as a:
                pickle.dump(array,a)
        ActHS()
        print(HS)
    
    def Mostrar():
        f = open("Archivo","rb")
        t = []
        while True: #check for end of file
            try:
                t.append(pickle.load(f)) # append record from file to end of list
            except EOFError:
                break
        f.close()
        for i in t:
            print(i, "\n")

class Fondo():
    def __init__(self) -> None:
        self.lista = []
        self.Estrellas()

        pass

    def Update(self):
        for i in self.lista:
            i.Update()

    def Estrellas(self):
        cant = 30
        for i in range(0,cant):
            self.lista.append(self.Estrella())

    class Estrella():
        def __init__(self) -> None:
            self.tam = random.randint(1,3)
            self.pos = (
                random.randint(0,WIDTH),
                random.randint(0,HEIGHT)
            )
            self.col = WHITE
            self.rect = pygame.rect.Rect(0,0,self.tam, self.tam)
            self.rect.center = self.pos
            pygame.draw.rect(screen, self.col, self.rect)
            pass

        def Update(self):
            self.rect.x -= self.tam
            pygame.draw.rect(screen, self.col, self.rect)

            if self.rect.right<0:
                self.rect.x = WIDTH
                self.rect.y = random.randint(0,HEIGHT)

class Trans():
    def __init__(self) -> None:
        
        pass

    def Salir():
        r = 100
        p = (WIDTH//2, HEIGHT//2)
        while True:
            pygame.time.delay(10)
            pygame.draw.circle(screen, BLACK, p, r, 100)
            pygame.display.flip()
            r += 10

            v = pygame.mixer.music.get_volume()
            pygame.mixer.music.set_volume(v-0.01)
            if r>WIDTH:
                break
        pass

    def Entrar(todos,fondo):
        r = WIDTH
        p = (WIDTH//2, HEIGHT//2)
        while True:
            screen.fill((10,10,10))
            todos.draw(screen)
            fondo.Update()
            pygame.time.delay(10)
            pygame.draw.circle(screen, BLACK, p, r,width=0)
            pygame.display.flip()
            r -= 10

            v = pygame.mixer.music.get_volume()
            pygame.mixer.music.set_volume(v+0.05)
            if r<1:
                break
        pass

class fuego():
    def __init__(self, Color=(255,255,255)):
        self.col = Color 
        self.p = []
        self.cor = (
            random.randint(0,WIDTH),
            random.randint(0,HEIGHT)
        )
        for i in range(0,10):
            self.p.append(self.particula(self.col,self.cor))
    
    def update(self):
        if len(self.p)==0:
            self = 0

        for i in self.p:
            if i.vi>=50:
                self.p.clear()
            else:
                i.update()
    
    class particula():
        def __init__(self, col, cor):
            self.col = col
            self.dir = random.randint(0,359)
            self.vi = 0
            self.cor = cor
         
        def update(self):
            vel = 5 
            self.cor = (
                self.cor[0]+int((math.cos(self.dir)*vel)),
                self.cor[1]+int((math.sin(self.dir)*vel))
            )

            pygame.draw.circle(screen,
                               self.col,
                               self.cor,
                               5,
                               5)

            self.vi += vel


#Del Juego

from logging import root
import pygame
import random
import math
from Data import *

Bnivel = 1
ts = 500
score = 0

BB = False

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter")
FONT = pygame.font.Font('freesansbold.ttf', 32)

#DEFINICIÓN DE CLASES/OBJETOS

#OBJETO DEL JUGADOR
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image0 = pygame.image.load("Assets/naveVer.png").convert()
        self.image0.set_colorkey(WHITE)
        self.image1 = pygame.image.load("Assets/naveInv.png").convert()
        self.image1.set_colorkey(BLACK)
        self.image = self.image0
        self.rect = self.image.get_rect()
        self.canon = self.rect.width - (self.rect.width*0.75)
        self.rect.width *= 0.75
        self.rect.centerx =  40
        self.rect.bottom = HEIGHT//2

        self.Ssh = pygame.mixer.Sound("Sonidos\Laser.ogg")
        
        self.ultB = pygame.time.get_ticks()
        self.cadn = 250
        self.vel = 10
        self.Balas = pygame.sprite.Group()
        self.Aura = pygame.sprite.Group()
        self.abri = 0
        self.temp = 0
        self.t = 1000
        self.bolas = 0
        self.Inve = 1000
        self.tb = 0
        self.TVb = 5000
        
        self.Vul = True
        self.gol = pygame.time.get_ticks()
        self.Vidas = 3

        self.yo = pygame.sprite.Group()
        self.yo.add(self)
        todos.add(self)

    def update(self):
        self.Movimiento()
        self.Coll()
        self.muerte()

        key = pygame.key.get_pressed()
        if key[pygame.K_s]:
            ahora = pygame.time.get_ticks()
            tempo = ahora - self.ultB

            if tempo>=self.cadn:
                self.Shot()

        if self.bolas>0:
            if self.bolas==1:
                self.b1 = self.Bolas()
                self.bolas += 1
            self.b1.update()

        if self.abri!=0 and self.temp==0:
            self.temp = self.t
        
        if self.temp!=0:
            if not BB: self.temp -= 1
            if self.temp==0:
                self.abri=0
    
    def Shot(self):
        pos = self.rect.midright
        var = random.randrange(-5,5)
        pos = [pos[0]+self.canon, pos[1]+var]
        Nbala = Bala(pos,0)
        pygame.mixer.Sound.play(self.Ssh,maxtime=ts)

        i =0
        while i<self.abri:
            pos = [pos[0]-1, pos[1]-1]
            Nbala1 =Bala(pos, 2)
            pos = [pos[0]-1, pos[1]-1]
            Nbala2 =Bala(pos, -2)
            i+=1
        
        self.Balas.add(Nbala)
        self.ultB = pygame.time.get_ticks()

    def Movimiento(self):
        #variables del objeto
        x = self.rect.x
        y = self.rect.y
        rect = self.rect
        #variables de movimiento
        vel = self.vel
        velx = 0
        vely = 0
        
        Ctop = rect.top<=0
        Cleft = rect.left<=0
        Cdwn = rect.bottom>=HEIGHT
        Crig = rect.right>=WIDTH
        key = pygame.key.get_pressed()
        if (key[pygame.K_UP]) and not Ctop:
            vely=-vel
        if key[pygame.K_DOWN] and not Cdwn:
            vely=+vel

        if (key[pygame.K_RIGHT]) and not Crig:
            velx=+vel
        if (key[pygame.K_LEFT]) and not Cleft:
            velx-=vel

        if velx != 0 and vely != 0:
            velx = (2 * math.sqrt(vel)) * (velx/abs(velx))
            vely = (2 * math.sqrt(vel)) * (vely/abs(vely))

        x += velx
        y += vely
        #devolver valores alterados
        self.rect.x = x
        self.rect.y = y
    
    def Coll(self):
        c = pygame.sprite.groupcollide(self.yo, enemigos, 0, 0)

        if c and self.Vul:
            Sonidos["golpe"].play()
            ret = self.rect.x - 50
            if ret<0:
                self.rect.x = 0
            else:
                self.rect.x -= 50
            self.Vidas -= 1
            self.Vul = False
            self.image = self.image1
            self.gol = pygame.time.get_ticks()

        now = pygame.time.get_ticks()
        tem = now-self.gol
        if not self.Vul and tem>= 500:
            if self.image == self.image0:
                self.image = self.image1
            else:
                self.image = self.image0
        if tem>= self.Inve:
            self.Vul = True
            self.image = self.image0
            self.Inve = 1000
    
    def muerte(self):
        if self.Vidas <= 0:
            Perder()

    class Bolas(pygame.sprite.Sprite):
        def __init__(self) -> None:
            super().__init__()
            self.image = pygame.image.load("Assets/Bola.png").convert()
            self.image.set_colorkey(WHITE)
            self.rect = self.image.get_rect()
            self.A = 0
            self.Nac = pygame.time.get_ticks()
            self.TV = player.TVb
            self.edad = self.TV

            todos.add(self)
            player.Aura.add(self)
            player.Balas.add(self)

            Sonidos["bolas"].play(maxtime=1000)
            pass

        def update(self):
            self.A +=1 
            A = self.A
            x = player.rect.x + int((math.cos(A)*150))
            y = player.rect.y + int((math.sin(A)*150))

            self.rect.x = x
            self.rect.y = y

            edad = pygame.time.get_ticks()-self.Nac
            player.tb = self.TV-edad
            if edad>=self.TV:
                self.kill()
                player.bolas = 0

    pass

#BALAS
class Bala(pygame.sprite.Sprite):
    def __init__(self, pos, abri):
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load("Assets/bala2.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.midleft = self.pos 

        player.Balas.add(self)
        todos.add(self)

        self.speed = 20
        self.desv = abri

    def update(self):
        self.rect.x += self.speed
        self.rect.y += self.desv

        if BB:
            r = Nboss.rect
            c = self.rect.colliderect(r)
            if c:
                if Nboss.vul:
                    Nboss.vida -= 1
                self.kill()

        if self.rect.x >= WIDTH+20:
            self.kill()

#ROCAS
class enemigo(pygame.sprite.Sprite):
    def __init__(self, IA = 0) -> None:
        super().__init__()
        r = 4
        if score >= 1000:
            r = 5
        if score >= 1500:
            r = 6

        if IA != 7:
            self.IA = random.randint(0,r)
        else: 
            self.IA = IA

        self.velY = 0
        self.ys = random.randrange(0,HEIGHT)
        self.xs = WIDTH
        self.Ibase = pygame.image.load("Assets/meteoro.png").convert()
        self.Iroto = pygame.image.load("Assets/meteoroR.png").convert()
        

        self.Edad = pygame.time.get_ticks()
        self.desc = self.Edad

        self.g = pygame.sprite.Group()
        self.g.add(self)

        self.vida = 1
        self.velO = 5 + score//200
        if self.velO>15:
            self.vel0 = 15

        self.vel = self.velO
        
        if self.IA == 2:
            self.ys = HEIGHT//2
            self.onda = random.randint(90,140)
        elif self.IA == 3:
            self.velY = 5
            self.velY *= random.choice([-1, 1])
        elif self.IA == 4:
            self.ys = random.choice([-20,HEIGHT+20])
            self.xs = random.randint(20,WIDTH)
        elif self.IA == 5:
            self.r = False
            self.velY = self.vel * 1.1
            self.velY *= random.choice([-1, 1])
        elif self.IA == 6:
            si = self.Ibase.get_rect().size
            self.Ibase = pygame.transform.scale(self.Ibase, (si[0]*3, si[1]*3))
            si = self.Iroto.get_rect().size
            self.Iroto = pygame.transform.scale(self.Iroto, (si[0]*3, si[1]*3))
        elif self.IA == 7:
            si = self.Ibase.get_rect().size
            self.Ibase = pygame.transform.scale(self.Ibase, (si[0]*0.8, si[1]*0.8))
            si = self.Iroto.get_rect().size
            self.Iroto = pygame.transform.scale(self.Iroto, (si[0]*0.8, si[1]*0.8))

        
        self.image = self.Ibase
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.xs
        self.rect.centery = self.ys
        
        #para la destruccion
        self.dest = False
        self.cont = 10

        pass

    def update(self):
        
        if not self.dest:
            self.Coll()
            vel = self.vel
            self.rect.x -= vel
            self.rect.y += self.velY
            I = self.IA
            if I==1:
                self.IA1()
            if I==2:
                self.IA2()
            if I==3:
                self.IA3()
            elif I==4:
                self.IA4()
            elif I==5:
                self.IA5()
            elif I==6:
                self.IA6()
            elif I==7:
                self.IA7()
        else: 
            self.CambioImagen()
            if self.cont==0:
                self.Destroy()
            else:
                self.cont -= 1
            
        if(self.rect.left<-100):
            self.Destroy()

    def Coll(self):
        global score
        c = False
        c = pygame.sprite.groupcollide(player.Balas, self.g, 1, 0) or pygame.sprite.groupcollide(player.Aura, self.g, 0, 1)
        
        if c:
           pygame.mixer.Sound.play(Sonidos["romper"],maxtime=ts)
           self.dest = True

    def IA1(self):
        x = self.rect.x
        pausa = WIDTH-100
        fin = 1000
        parar = True
        edad = self.Edad

        if x<=pausa and parar: 
            self.vel = 0

        A = pygame.time.get_ticks()
        T = A - edad
        if T>=fin:
            parar = False

        if not parar:
            self.vel = self.velO*3



        pass
    
    def IA2(self):
        self.vel = 2 + score//200
        x = self.rect.x
        onda = self.onda
        y = math.sin(x/onda) * 250
        self.rect.centery = self.ys+y

    def IA3(self):
        if self.rect.top<=0 or self.rect.bottom>=HEIGHT:
            self.velY *= -1

        self.rect.y += self.velY

    def IA4(self):
        y = (5 + score//200)
        if self.ys!=0:
            y *= -1
        self.vel *= 0.80

        self.rect.y += y
        pass

    def IA5(self):
        if self.rect.top<0:
            self.rect.top = 0
        if self.rect.bottom>HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top==0 or self.rect.bottom==HEIGHT:
            self.velY *= -1
        if self.rect.left <= 0:
            self.vel *= -1
            self.r = True
        if self.rect.right>=WIDTH and self.r:
            self.vel *= -1

    def IA6(self):
        self.vel = self.velO//2
        pass
    
    def IA7(self):
        self.velY *= 0.96
        self.vel = self.velO*1.2
        pass

    def Destroy(self):
        global score

        if(self.rect.x > 0):
             score += 10
             aux = random.randint(0,14)
             if aux == 1:
                 power = PowerUp(self.rect.centerx, self.rect.centery)

        if(self.IA == 6):
            for i in range(0,2):
                mono = enemigo(IA = 7)
                mono.IA = 7
                mono.rect.center = self.rect.center
                mono.velY = 5 - 10*i
                enemigos.add(mono)
                colisionables.append(mono)
                todos.add(mono)

        self.kill()
        pass
    
    def CambioImagen(self):
        c = self.rect.center
        self.image = self.Iroto
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = c

#Jefe y sus objetos
class Boss(pygame.sprite.Sprite):
    def __init__(self, n) -> None:
        super().__init__()
        global BB
        BB = True
        #grupos
        self.g = pygame.sprite.Group()
        self.g.add(self)
        todos.add(self)

        #geometria
        self.image = pygame.image.load("Assets/Jefe.png")
        self.image = pygame.transform.scale(self.image, (200,300))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH+100, HEIGHT//2)

        self.fase = 0
        self.vel = 0
        self.acc = 0.5
        self.vidaI = 150*n
        self.vida = self.vidaI
        self.CadD = 500
        self.ultAtaque = pygame.time.get_ticks()
        self.vul = False
        
        pygame.mixer.music.pause()
        pygame.mixer.Sound.play(Sonidos["boss"])

    def update(self):
        self.Vida()
        if self.fase==0:
            self.Fase0()
        if self.fase==1:
            self.Fase1()
        if self.fase==2:
            self.Fase2()
        if self.fase==3:
            self.Fase3()
 
    def Fase0(self):
        self.pos = WIDTH*0.90-self.rect.width
        if(not enemigos.has(self)):
            enemigos.add(self)
        if(self.rect.x<=self.pos):
            Sonidos["boss"].stop()
            pygame.mixer.music.unpause()
            self.fase = 1
            self.Tdis = pygame.time.get_ticks()
        else:
            self.rect.x -= 1
    
    def Fase1(self):
        Sonidos["boss"].stop()
        self.vul = True
        #Movimiento
        max = 15
        acc = self.acc
        vel = self.vel
        if self.rect.y <= 50 and acc<0:
            acc *= -1
        if self.rect.bottom >= HEIGHT-50 and acc>0:
            acc *= -1
        maxv = max*acc
        if vel!=maxv:
            vel += acc
        self.rect.y += vel
        self.vel = vel
        self.acc = acc
        #ataque
        t = pygame.time.get_ticks() - self.Tdis
        if t>= self.CadD:
            Sonidos["bDisparo"].play(maxtime=500)
            b = BBala(self.rect.x, self.rect.y)
            b1 = BBala(self.rect.x, self.rect.bottom)
            self.Tdis = pygame.time.get_ticks()

        #Fin
        if self.vida<=self.vidaI*0.66:
            self.fase += 1

    def Fase2(self):
        #movimiento
        mitad = HEIGHT//2
        vel = (self.rect.centery-mitad)//2
        self.rect.y -= vel
        
        #ataque
        Tataque = 2000
        if (pygame.time.get_ticks()-self.ultAtaque)>=Tataque:
            miniom = BMiniom()
            miniom1 = BMiniom()
            self.ultAtaque = pygame.time.get_ticks()

        if(self.vida<=self.vidaI*0.33):
            self.fase += 1

    def Fase3(self):
        #movimiento
        
        #ataque
        Tataque = 2000
        if (pygame.time.get_ticks()-self.ultAtaque)>=Tataque:
            miniom = BMiniom()
            miniom1 = BMiniom()
            miniom2 = BMiniom()
            self.ultAtaque = pygame.time.get_ticks()

    def Vida(self):
        porc = self.vida/self.vidaI
        rect = pygame.rect.Rect(0,HEIGHT-20,WIDTH*porc,10)
        pygame.draw.rect(screen, (255,0,0), rect)

        if self.vida<=0:
            self.vul = False
            if(enemigos.has(self)):
                enemigos.remove(self)
            if(Sonidos["bDerrota"].get_num_channels()<1):
                Sonidos["bDerrota"].play()
            self.fase = -1
            self.rect.y += 1
            self.rect.x -= 2
            if self.rect.y >= WIDTH+2:
                self.derrota()

    def derrota(self):
        global jefe
        global BB
        global score

        Sonidos["bDerrota"].stop()
        self.kill()
        score += 500
        jefe = score+1000
        BB = False

    pass

#BALAS DEL JEFE
class BBala(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        #Visual
        self.image = pygame.image.load("Assets/bala.png").convert()
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        #Grupos
        enemigos.add(self)
        todos.add(self)

        #Variables
        self.velX = 15

        pass

    def update(self):
        self.rect.x -=self.velX
        if self.rect.x <= -50:
            self.kill()

#MINI NAVES DEL JEFE
class BMiniom(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Assets/nave.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = Nboss.rect.center

        self.paso = 0
        self.pos = random.randrange(0, Nboss.pos) 
        self.pausa = 1500
        self.rayo = None
        self.ata = False

        todos.add(self)
    
    def update(self):
        velX = 0
        velY = 0
        if self.paso==0:
            velX = 10
            if self.rect.x >= WIDTH:
                self.paso += 1
        if self.paso==1:
            velX = 0
            velY = -10
            if self.rect.top<=0:
                self.paso += 1
        if self.paso==2:
            velY = 0
            velX = -10
            if self.rect.x <= self.pos:
                self.paso += 1
                self.inPausa = pygame.time.get_ticks()
        if self.paso==3:
            velX = 0
            now = pygame.time.get_ticks()
            tempo = now-self.inPausa
            if tempo>=self.pausa//2:
                
                if self.ata == False:
                    Sonidos["bMiniom"].play()
                    self.rayo = self.laser(self.rect.centerx,self.rect.bottom)
                    self.ataque()
                    self.ata = True
            if tempo>=self.pausa:
                self.rayo.destroy()
                self.paso += 1
        if self.paso==4:
            self.rayo.kill()
            velX = -15
            if self.rect.x<=-50:
                self.kill()
        
        self.rect.x += velX
        self.rect.y += velY

    def ataque(self):
        pass
    
    class laser(pygame.sprite.Sprite):
        def __init__(self, x,y) -> None:
            super().__init__()
            self.image = pygame.image.load("Assets/laser.png").convert()
            self.image = pygame.transform.scale(self.image, (64,WIDTH))
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.y = y
            self.time = 500
            self.ini = pygame.time.get_ticks()

            todos.add(self)
            enemigos.add(self)

        def update(self):
            
            if (pygame.time.get_ticks()-self.ini)>=self.time:
                self.kill()
            pass

        def destroy(self):
            self.kill()

#PODERES
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x,y):
        super().__init__()
        tipo = self.Tipo()


        self.tipo = tipo
        sprite = [
            "Assets/Power0.png",
            "Assets/Power1.png",
            "Assets/Power2.png",
            "Assets/Power3.png",
            "Assets/Power4.png",
            "Assets/Power5.png"
        ]
        self.image = pygame.image.load(sprite[tipo]).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        todos.add(self)
        self.bonus = pygame.sprite.Group()
        self.bonus.add(self)

    def Tipo(self):
        A = player.cadn>50
        B = player.Vidas<5
        C = player.abri<1
        D = player.bolas==0
        E = 1==random.randint(0,1)
        lis = []
        
        if A:
            lis.append(0)
        if B:
            lis.append(1)
        if C:
            lis.append(2)
        if D:
            lis.append(3)
        elif E:
            lis.append(4)

        if len(lis)==0:
            return 5
        else:
            return random.choice(lis)

    def update(self):
        self.rect.x -= 5 
        self.Coll()
    
    def Coll(self):
        global score 
        c = pygame.sprite.groupcollide(self.bonus, player.yo, 0, 0, collided = None)
        if c:
            Sonidos["bonus"].play()
            if self.tipo==0:
                print("+Velocidad")
                player.cadn *= 0.90
                player.vel += 1
            if self.tipo==1:
                print("+Vida")
                player.Vidas += 1
            if self.tipo==2:
                print("+dispercion")
                player.abri += 1
            if self.tipo==3:
                print("Aura")
                player.bolas = 1
            elif self.tipo==4:
                print("Invencibilidad")
                player.Vul = False
                player.Inve = 5000
                player.gol = pygame.time.get_ticks()
            if self.tipo==5:
                print("+puntos")
                score+=50
        
            
            score += 50
            self.kill()

#DIBUJAR LA INTERFAZ (VIDAS, PUNTOS, ETC) 
class GUI():
    def __init__(self) -> None:
        super().__init__()
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        pass

    def update(self):
        self.vidas()
        self.puntos()
        self.power()

        pass

    def power(self):
        pos = 1
        if not player.Aura.empty():
            s = player.tb/player.TVb
            t = iPower2.get_size()
            imagen = pygame.transform.scale(iPower3, (t[0]*s, t[1]*s))
            r = imagen.get_rect()
            r.center = (WIDTH-70 ,HEIGHT-70)
            screen.blit(imagen, r)
            pos += 1
        
        if player.abri > 0:
            s = player.temp/player.t
            t = iPower2.get_size()
            imagen = pygame.transform.scale(iPower2, (t[0]*s, t[1]*s))
            r = imagen.get_rect()
            r.center = (WIDTH-70*pos ,HEIGHT-70)
            screen.blit(imagen, r)

        pass

    def vidas(self):
        posx = 10
        espacio = Ividas.get_rect().width + 10
        for i in range(0,player.Vidas):
            screen.blit(Ividas,(posx,10))
            posx += espacio
        pass

    def puntos(self):
        txt = "Score {}".format(score)
        font = self.font
        texto = font.render(txt, True,WHITE)
        rect = texto.get_rect()
        rect.x = 50
        rect.y = HEIGHT-50
        screen.blit(texto, rect)

#FUNCION QUE GUARDA LOS DATOS AL PERDER
def Perder():
    global SCORE
    global imagen
    Tablero.Guardar(score)
    ActHS()
    SCORE = score
    print("Score: ",SCORE)
    print("--GAME OVER--")
    imagen = pygame.image.save(screen, "fin.jpg")
    global run
    run = False

#FUNCION PARA GANAR Y SUS VARIABLES
radio = (HEIGHT//2)**2 + (WIDTH//2)**2
radio = math.sqrt(radio)
radio = float(radio)
f = fuego(Color=(
    random.choice([0,255]),
    random.choice([0,255]),
    random.choice([0,255])
))
planetaX = WIDTH+radio
planetaY = HEIGHT//2
vuelta = 0
def Ganar():
    global planetaX
    global f
    car = Cartel("Fin del Juego", 60, WIDTH//2, HEIGHT*0.33, central=True)
    
    pygame.draw.circle(screen, 
                       (50,50,150),
                       (planetaX,planetaY),
                       radio,
                       int(radio))
    
    pygame.draw.circle(screen, 
                       (186,74,0),
                       (planetaX-200,planetaY-200),
                       250,
                       250)
    
    pygame.draw.circle(screen, 
                       (30, 132, 73),
                       (planetaX-200,planetaY-200),
                       220,
                       220)
    
    pygame.draw.circle(screen, 
                       (186,74,0),
                       (planetaX+105,planetaY+250),
                       100,
                       100)
    
    pygame.draw.circle(screen, 
                       (46, 204, 113),
                       (planetaX+105,planetaY+250),
                       70,
                       70)
    
    pygame.draw.circle(screen, 
                       (186,74,0),
                       (planetaX+170,planetaY+40),
                       100,
                       100)
    
    pygame.draw.circle(screen, 
                       (46, 204, 113),
                       (planetaX+170,planetaY+40),
                       70,
                       70)
    
    
    if planetaX <= WIDTH//2:
        global vuelta
        vuelta += 1
    else:
        planetaX -= 3

    
    if vuelta==250:
        global run 
        run = False

#GRUPOS DE PYGAME Y LISTAS
todos = pygame.sprite.Group()
enemigos = pygame.sprite.Group()
Balas = []
colisionables = []

#CREACION DE OBJETOS DE TIPO JUGADOR Y GUI
player = Player()
gui = GUI()

#FUNCION QUE EJECUTA EL PROPIO JUEGO
def Juego():
    #VARIABLES QUE SE USAN EN EL BUCLE
    global ultEne
    global run 
    global player
    global score
    global enemigos
    global todos
    global jefe
    global BB
    global Bnivel
    global Win 
    Win = False
    Bnivel = 1
    todos.empty()
    enemigos.empty()
    run =True
    ultEne = pygame.time.get_ticks()
    TenEn = 900
    jefe = 500
    player.__init__()
    score = 0
    fondo = Fondo()
    gano = 0
    pygame.mixer.music.load("Sonidos/Fondo.mp3")
    pygame.mixer.music.set_volume(0)
    pygame.mixer.music.play(-1)
    Trans.Entrar(todos,fondo)
    
    #FUNCIONES QUE USA EL BUCLE

    #FUNCIÓN QUE CREA UN TIPO DE ENEMIGO
    def crearEn():
        T = TenEn-(score//50) #DEFINIMOS CADA CUANTO VAMOS A CREAR UN ENEMIGO

        #EL TIEMPO ENTRE ENEMIGOS NO PUEDE SER MENOR A 100 MILISEGUNDOS
        if T<100: #SI EL TIEMPO ES MENOR A CIEN
            T=100 #SE FIJA EN 100

        now = pygame.time.get_ticks() #SE TOMA EL TIEMPO DE AHORA
        
        tempo = now-ultEne #SE REVISA CUANTO TIEMPO PASO DESDE EL ULTIMO ENEMIGO HASTA AHORA
        if tempo>=T: # SE PASO DEL TIEMPO QUE DEFINIMOS ENTRE ENEMIGOS
            if not BB: #SI NO ES MOMENTO DE UN JEFE 
                crearMeteoro()#SE CREA UN METEORO
            if score>=jefe: #SI EL PUNTAJE LLEGA A CIERTO VALOR
                crearBoss() #SE INVOCA AL JEFE
        
    #ESTA FUNCION CREA UN METEORO
    def crearMeteoro():
        global ultEne
        mono = enemigo()#SE CREA UN ENEMIGO

        #SE LO AÑADE A LOS GRUPOS A LOS QUE CORRESPONDA
        enemigos.add(mono)
        colisionables.append(mono)
        todos.add(mono)

        #DAMOS EL TIEMPO EN QUE SE CREA
        ultEne = pygame.time.get_ticks()

    #ESTA CREA UN JEFE
    def crearBoss():
        if not BB:#SI NO HAY UN JEFE EN PANTALLA
            global Nboss 
            global Bnivel
            Nboss = Boss(Bnivel) #CREA UN JEFE PASANDOLE SU NIVEL DE DIFICULTAD
            Bnivel += 1 #SE AUMENTA LA DIFICULTAD PARA EL SIGUIENTE JEFE
    
    #ESTA FUNCION EMITE UN MENSAJE POR CONSOLA
    #LO USAMOS DURANTE LAS PRUEBAS PARA DETECTAR ERRORES, SABER SI UNA PARTE DEL CODIGO FUNCIONA, ETC.
    print("Empieza el Juego")
    
    #ESTA PARTE DE CODIGO SE REPITE EN BUCLE
    #ESTE BUCLE HACE QUE EL JUEGO SE EJECUTE
    while(run):
        clock.tick(60)#ESTO HACE QUE LA VELOCIDAD DEL PROGRAMA SE LIMITE A 60 VUELTAS POR SEGUNDO
        screen.fill((10,10,10))#LA PANTALLA SE LLENA CON NEGRO
        fondo.Update()#SE DIBUJA UN FONDO (EL OBJETO FONDO SE DEFINIO EN UN ARCHIVO DISTINTO IMPORTADO)

        #SE DETECTAN LAS ACCIONES DEL USUARIO
        for event in pygame.event.get():
            if event.type == pygame.QUIT:#SI EL USUARIO CIERRA LA VENTANA SE TERMINA EL BUCLE Y SE CIERRA EL PROGRAMA
                pygame.quit()
                run = False
                pass
            
        #TERMINAS EL JUEGO
        if Bnivel==6 and BB==False:#SI DERROTAS A 5 JEFES
            Win = True#GANAS EL JUEGO
            gano = 1#SE LE DISE AL OTRO ARCHIVO QUE GANASTE
        
        if not Win:#SI NOGANASTE TODAVIA
            crearEn()#SE CREA UN ENEMIGO
        else:#SI NO
            Ganar() #GANAS EL JUEGO

        
        todos.draw(screen)#SE DIBUJAN TODOS LOS OBEJETOS EN LA PANTALLA
        todos.update()#SE EJECUTAN TODOS LOS "UPDATE" DE LOS OBJETOS
        gui.update()#SE ACTUALIZA LA GUI EN CADA VUELTA
        pygame.display.flip()#SE ACTUALIZA LA PANTALLA
        pass
    
    #CUANDO EL BUCLE TERMINA SE APAGA LA CREACION DE ENEMIGO Y SE PASA A OTRO ARCHIVO
    #EL PUNTAJE Y SI SE LLEGO AL FINAL O NO
    BB = False
    pasar = [score, gano]
    return pasar
    

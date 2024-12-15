import pygame
import pickle
from os import system
from Data import *
system("cls")

pygame.init()
pygame.display.set_caption("Shooter")
pygame.mixer.init()
musica = pygame.mixer.music.load("Sonidos/musica1.mp3")
pygame.mixer.music.play( -1)
pygame.mixer.music.set_volume(2)

boton1 = Boton("Salir",WIDTH//2,500)
boton2 = Boton("Jugar",WIDTH//2,300)

cartel1 = Cartel("High Score: ", 32, 10, HEIGHT-80)


def botones():
    global run
    
    boton2.Actualizar(screen)
    boton1.Actualizar(screen)

    if boton1.Press:
        return 1
    elif boton2.Press:
        return 2
    else: 
        return 0
def GUI():
    hs = ActHS()
    cartel2 = Cartel(str(hs), 32, 10, HEIGHT-40)
    cartel1.draw()
    cartel2.draw()

run =True
def Menu():
    ActHS()
    fondo = Fondo()
    musica = pygame.mixer.music.load("Sonidos/musica1.mp3")
    pygame.mixer.music.play(-1)
    
    global run
    run = True
    boton = 0

    while(run):
        screen.fill([10,10,10])
        fondo.Update()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                pass

        GUI()
        boton = botones()
        
        if boton!=0:
            run = False
        pygame.display.flip()
        pass
    if boton == 2:
        Trans.Salir() 

    return boton


#Naves.Juego()

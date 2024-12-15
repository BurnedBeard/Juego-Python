import Menu
import Naves
import GameOver
import pygame
from os import system
system("cls")
 
pygame.init()

while True:
    o = Menu.Menu()
    if o==1:
        break
    else:
        while True:
            s = Naves.Juego()
            o = GameOver.Pan(s)
            if o==1:
                break

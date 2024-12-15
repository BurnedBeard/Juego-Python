import pygame
from Data import *

pygame.init()
musica = "Sonidos/MusicaGO.mp3"


bRejugar = Boton("Rejugar", WIDTH*0.33, HEIGHT*0.80)
bSalir = Boton("Volver", WIDTH*0.66, HEIGHT*0.80)

nuevo = Cartel("¡Nuevo Record!", 50, WIDTH//2, HEIGHT//2, central = True)
mensaje = Cartel("Perdiste", 100, WIDTH//2,HEIGHT*0.33, central=True)
score = SCORE
cele = False


def botones():
     bRejugar.Actualizar(screen)
     bSalir.Actualizar(screen)

     a = 0
     if bSalir.Press:
         a = 1
     elif bRejugar.Press:
         a = 2
     
     return a

def Carteles(s):
     global f
     global cele 
     if s[1] == 1:
          if len(f.p)==0:
               f = fuego(Color=(
                    random.choice([0,255]),
                    random.choice([0,255]),
                    random.choice([0,255])
               ))
          else:
               f.update()
          mensaje.texto = "Fin del Juego"
     else:
          mensaje.texto = "perdiste"
     mensaje.draw()
     if s[0]>HS:
          nuevo.draw()
          if not cele:
               bonus.play()
               cele = True
     
     pygame.display.update()
     
          
f = fuego(Color=(
     random.choice([0,255]),
     random.choice([0,255]),
     random.choice([0,255])
))
def Pan(s):
     run = True
     pygame.mixer.music.load(musica)
     pygame.mixer.music.play(-1,0.02, 1000)
     pygame.image.save(screen, "fin.jpg")
     imagen = pygame.image.load("fin.jpg")
     while run:
          
          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                    pass

          pygame.display.flip()
          screen.blit(imagen, (0,0))
          boton = botones()
          Carteles(s)
          if boton!=0:
               run = False

          pass
     if boton==2:
          Trans.Salir() 
     
     return boton

print("Cargado")
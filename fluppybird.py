
import pygame
import random

pygame.init()
pygame.mixer.init()
#upload immagini
sfondo = pygame.image.load('assets/sfondo.png') 
uccello = pygame.image.load('assets/bird.png')
base = pygame.image.load('assets/base.png')
gameover = pygame.image.load('assets/gameover.png')
tubo_giu = pygame.image.load('assets/tubo.png')
tubo_su = pygame.transform.flip(tubo_giu, False, True) # immagine,flip orizzonale, flip verticale

pygame.mixer.music.load("assets/soud_background.wav")
pygame.mixer.music.set_volume(0.1)  


#costanti
screen = pygame.display.set_mode((288, 512))
fps=50
vel= 3
font= pygame.font.SysFont('Arial', 50, bold=True)

class tubi_classe:
    def __init__(self):
        self.x = 300
        self.y = random.randint(-75, 150)
    def genera_tubi(self):
        self.x -= vel
        screen.blit(tubo_giu, (self.x, self.y + 210))
        screen.blit(tubo_su, (self.x, self.y - 210))
    def schianto(self,uccello, uccello_x, uccello_y):
        hitbox_uccello= 5
        uccello_lato_dx= uccello_x + uccello.get_width() - hitbox_uccello
        uccello_lato_sx= uccello_x + hitbox_uccello
        uccello_lato_su= uccello_y + hitbox_uccello
        uccello_lato_giu= uccello_y + uccello.get_height() - hitbox_uccello
        tubo_lato_dx= self.x + tubo_giu.get_width()
        tubo_lato_sx= self.x
        tubo_su_lato_giu= self.y + 110
        tubo_giu_lato_su= self.y + 210
        if uccello_lato_dx > tubo_lato_sx and uccello_lato_sx < tubo_lato_dx:
            if uccello_lato_su < tubo_su_lato_giu or uccello_lato_giu > tubo_giu_lato_su:
                stop()
    def passato(self, uccello, uccello_x):
        hitbox_uccello= 5
        uccello_lato_dx= uccello_x + uccello.get_width() - hitbox_uccello
        uccello_lato_sx= uccello_x + hitbox_uccello
        tubo_lato_dx= self.x + tubo_giu.get_width()
        tubo_lato_sx= self.x
        if uccello_lato_dx > tubo_lato_sx and uccello_lato_sx < tubo_lato_dx:
            return True
def avvio():
    global uccello_x, uccello_y, uccello_vel 
    global base_x, base_y
    global tubi
    global point
    global passato
    uccello_x = 60
    uccello_y = 150
    uccello_vel = 0
    base_x=0
    base_y=400
    tubi = []
    tubi.append(tubi_classe())
    point = 0
    passato=False
    pygame.mixer.music.play(-1)
avvio()

def aggiorna():
    pygame.display.update()
    pygame.time.Clock().tick(fps)

def caricaOggetti():
    screen.blit(sfondo, (0,0))
    for t in tubi:
        t.genera_tubi()
    screen.blit(uccello, (uccello_x, uccello_y))
    screen.blit(base, (base_x, base_y))
    conta_punti = font.render(str(point), True, (255,255,255))
    screen.blit(conta_punti, (135,0))

def stop():
    screen.blit(gameover, (50,200))
    pygame.mixer.music.stop()
    aggiorna()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    avvio()
                    return
            

while True: 
    base_x -= vel
    if base_x <= -45:
         base_x = 0

    #Gravità 
    uccello_vel += 0.5
    uccello_y += uccello_vel #porta l uccello verso il basso
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                uccello_vel = -5 #da una velocità di discesa negativa , di conseguenza si muove verso l'alto

    if tubi[-1].x < 150:
        tubi.append(tubi_classe())
    for t in tubi:
        t.schianto(uccello, uccello_x, uccello_y)
    if not passato:
        for t in tubi:
            if t.passato(uccello, uccello_x):
                passato= True
                break
    if passato:
        passato= False
        for t in tubi:
            if t.passato(uccello, uccello_x):
                passato= True
                break
        if not passato:
            point += 1

    if uccello_y > base_y:
        stop()

    caricaOggetti()
    aggiorna()

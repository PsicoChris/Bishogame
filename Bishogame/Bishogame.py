import pygame,sys
from pygame.locals import *
from random import randint


ancho = 850
alto =480
lista_enemy = []

class bishoSiu(pygame.sprite.Sprite):

    def __init__ (self):
        pygame.sprite.Sprite.__init__(self)
        self.ImagenBisho = pygame.image.load('imgsonly/bisho.png')

        self.rect = self.ImagenBisho.get_rect()
        self.rect.centerx = ancho/2
        self.rect.centery = alto-30

        self.listaDisparo = []
        self.Vida = True

        self.velocidad = 20
    def movDer (self):
        self.rect.right += self.velocidad
        self.__movimiento()
        
    def movIzq (self):
        self.rect.left -= self.velocidad
        self.__movimiento()


    def __movimiento(self):
        if self.Vida == True:
            if self.rect.left <= -40:
                self.rect.left = -40
            elif self.rect.right >= 920:
                self.rect.right = 920

    def cabecear(self,x,y):
        mibalon = Balon(x,y,'imgsonly/ball.png',True)
        self.listaDisparo.append(mibalon)
        print('¡El Bisho cabecea Dios mío!')
    
    def destruccion(self):
        self.Vida = False
        self.velocidad = 0

    def dibujar (self, superficie):
        superficie.blit (self.ImagenBisho, self.rect)

class noCreyente(pygame.sprite.Sprite):
    def __init__(self, posx, posy, distancia, imguno, imgdos):
        pygame.sprite.Sprite.__init__(self)

        self.imgBalOr = pygame.image.load(imguno)
        self.imgBal2 = pygame.image.load(imgdos)

        
        self.listaimgs = [self.imgBalOr, self.imgBal2]
        self.posImg = 0
        
        self.imgnocreyente = self.listaimgs[self.posImg]
        self.rect = self.imgnocreyente.get_rect()  

        self.listaDisparo = []
        self.velocidad = 2
        self.rect.top = posy
        self.rect.left = posx

        self.rangodisparo = 1
        self.tiempocambio = 1

        self.conquista = False

        self.derecha = True
        self.contador = 0
        self.Maxdes = self.rect.top + 40

        self.limiteder = posx + distancia
        self.limiteizq = posx - distancia
    
    def dibujar(self, superficie):
        self.imgnocreyente = self.listaimgs[self.posImg]
        superficie.blit(self.imgnocreyente, self.rect)

    def comport (self, tiempo):
        if self.conquista == False:
            self.__movimientos()

            self.__ataque()
            if self.tiempocambio == tiempo:
                self.posImg +=0.5
                self.tiempocambio +=0.5

                if self.posImg > len(self.listaimgs)-1:
                    self.posImg =0

    def __movimientos(self):        
        if self.contador < 3:
            self.__movimientolateral()
        else:
            self.__descenso()

    def __descenso(self):
        if self.Maxdes == self.rect.top:
            self.contador = 0
            self.Maxdes = self.rect.top +40
        else:
            self.rect.top += 1

    def __movimientolateral(self):
        if self.derecha == True:
            self.rect.left = self.rect.left + self.velocidad
            if self.rect.left > self.limiteder:
                self.derecha = False
                self.contador += 1
        else:
            self.rect.left = self.rect.left - self.velocidad
            if self.rect.left < self.limiteizq:
                self.derecha = True


    def __ataque(self):
        if (randint(0,100)<self.rangodisparo):
            self.__disparo()

    def __disparo(self):
        x,y = self.rect.center
        miproyectil = Balon(x,y, 'imgsonly/nouu.png', False)
        self.listaDisparo.append(miproyectil)

class Balon(pygame.sprite.Sprite):
    def __init__(self, posx, posy, ruta, personaje):
        pygame.sprite.Sprite.__init__(self)

        self.imgBalon = pygame.image.load(ruta)


        self.rect = self.imgBalon.get_rect()

        self.velocitydisp = 5

        self.rect.top = posy
        self.rect.left = posx

        self.dispPersonaje = personaje

    
    def trayectoria(self):
        if self.dispPersonaje == True:
            self.rect.top = self.rect.top - self.velocitydisp
        else:    
            self.rect.top = self.rect.top + self.velocitydisp
    
    def dibujar(self, superficie):
        superficie.blit(self.imgBalon, self.rect)

def detener():
    for enemigo in lista_enemy:
        for disparo in enemigo.listaDisparo:
            enemigo.listaDisparo.remove(disparo)

def cargar_enemigos():
    posx = 100
    for x in range (1,5):
        enemigo = noCreyente (posx,100,40, 'imgsonly/ballgold.png', 'imgsonly/nocr01.png')
        lista_enemy.append(enemigo)
        posx = posx + 200

    posx = 100
    for x in range (1,5):
        enemigo = noCreyente (posx,0,40, 'imgsonly/agua.png', 'imgsonly/coca.png')
        lista_enemy.append(enemigo)
        posx = posx + 200

    posx = 100
    for x in range (1,5):
        enemigo = noCreyente (posx,-100,40, 'imgsonly/canchis.png', 'imgsonly/canchis2.png')
        lista_enemy.append(enemigo)
        posx = posx + 200

def BishoGame():
    pygame.init()
    ventana = pygame.display.set_mode((ancho,alto))
    pygame.display.set_caption("Bishogame")

    fondoimagen = pygame.image.load('imgsonly/estadio.jpg')
    mifuentesys = pygame.font.SysFont("Times New Roman", 50)
    text = mifuentesys.render("Fin del Juego", 0, (120,100,40))

    jugador = bishoSiu()
    cargar_enemigos()

    enjuego = True
    reloj = pygame.time.Clock()

    while True:

        reloj.tick(60)
        tiempo = pygame.time.get_ticks()/1000


        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if enjuego == True:
                if event.type == pygame.KEYDOWN:

                    if event.key == K_LEFT:
                        jugador.movIzq()

                    elif event.key == K_RIGHT:
                        jugador.movDer()

                    elif event.key == K_c:
                        x,y = jugador.rect.center
                        jugador.cabecear(x,y)

        
        ventana.blit(fondoimagen, (0,0))

        jugador.dibujar(ventana)


        if len(jugador.listaDisparo)>0:
            for x in jugador.listaDisparo:
                x.dibujar(ventana)
                x.trayectoria()
                if x.rect.top < 10:
                    jugador.listaDisparo.remove(x)
                else:
                    for enemigo in lista_enemy:
                        if x.rect.colliderect(enemigo.rect):
                            lista_enemy.remove(enemigo)
                            jugador.listaDisparo
        
        if len(lista_enemy)>0:
            for enemigo in lista_enemy:
                enemigo.comport(tiempo)
                enemigo.dibujar(ventana)
            if enemigo.rect.colliderect(jugador.rect):
                jugador.destruccion()
                jugador.listaDisparo.remove(disparo)
                enemigo.listaDisparo.remove(x)

            if len(enemigo.listaDisparo)>0:
                for x in enemigo.listaDisparo:
                    x.dibujar(ventana)
                    x.trayectoria()
                    if x.rect.colliderect(jugador.rect):
                        jugador.destruccion()
                        enjuego = False
                        detener()
                    if x.rect.top < 20:
                        enemigo.listaDisparo.remove(x)
                    else:
                        for disparo in jugador.listaDisparo:
                            pass


        if enjuego == False:
            ventana.blit(text,(300,300))


        pygame.display.update()

BishoGame()
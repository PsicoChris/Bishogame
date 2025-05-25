import pygame, sys
from pygame.locals import *
from random import randint
import os # Para verificar si el archivo de puntuaciones existe

# --- Constantes del Juego ---
ANCHO = 850
ALTO = 480

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS_OSCURO = (120, 100, 40)
VERDE_PUNTOS = (0, 200, 0)
AZUL_CLARO = (173, 216, 230) # Para los botones
GRIS_CLARO = (200, 200, 200) # Para los botones al pasar el ratón

# Velocidades
VELOCIDAD_JUGADOR = 15
VELOCIDAD_BALON_JUGADOR = 10
VELOCIDAD_BALON_ENEMIGO = 5
VELOCIDAD_ENEMIGO_MOV = 2
DESPLAZAMIENTO_VERTICAL_ENEMIGO = 40

# Rutas de Imágenes
IMAGEN_BISHO = 'imgsonly/bisho.png'
IMAGEN_BALON_JUGADOR = 'imgsonly/ball.png'
IMAGEN_DISPARO_ENEMIGO = 'imgsonly/nouu.png'
IMAGEN_FONDO = 'imgsonly/estadio.jpg'

# Imágenes de Enemigos
ENEMIGO_TIPOS = [
    {'img1': 'imgsonly/ballgold.png', 'img2': 'imgsonly/nocr01.png', 'y_offset': 100, 'puntos': 10},
    {'img1': 'imgsonly/agua.png', 'img2': 'imgsonly/coca.png', 'y_offset': 0, 'puntos': 20},
    {'img1': 'imgsonly/canchis.png', 'img2': 'imgsonly/canchis2.png', 'y_offset': -100, 'puntos': 30},
]

# Archivo de Puntuaciones
ARCHIVO_PUNTUACIONES = 'puntuaciones.txt'
MAX_PUNTUACIONES = 5 # Cuántas puntuaciones máximas guardar

# --- Clases del Juego (sin cambios en su lógica interna) ---

class BishoSiu(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(IMAGEN_BISHO).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.centery = ALTO - 30
        self.velocidad = VELOCIDAD_JUGADOR
        self.vida = True

    def update(self):
        if self.vida:
            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > ANCHO:
                self.rect.right = ANCHO

    def movDer(self):
        if self.vida:
            self.rect.x += self.velocidad

    def movIzq(self):
        if self.vida:
            self.rect.x -= self.velocidad

    def cabecear(self):
        if self.vida:
            return Balon(self.rect.centerx, self.rect.top, IMAGEN_BALON_JUGADOR, True)
        return None

    def destruir(self):
        self.vida = False
        self.velocidad = 0

class noCreyente(pygame.sprite.Sprite):
    def __init__(self, posx, posy, distancia, imguno, imgdos, puntos):
        super().__init__()
        self.images = [pygame.image.load(imguno).convert_alpha(), pygame.image.load(imgdos).convert_alpha()]
        self.posImg = 0
        self.image = self.images[self.posImg]
        self.rect = self.image.get_rect()
        self.rect.top = posy
        self.rect.left = posx

        self.velocidad = VELOCIDAD_ENEMIGO_MOV
        self.rango_disparo = 1
        self.ultimo_cambio_img = 0
        self.tiempo_cambio_img = 200

        self.derecha = True
        self.contador_mov_lateral = 0
        self.max_descenso_actual = self.rect.top + DESPLAZAMIENTO_VERTICAL_ENEMIGO

        self.limiteder = posx + distancia
        self.limiteizq = posx - distancia
        self.puntos = puntos

    def update(self, current_time):
        if self.contador_mov_lateral < 3:
            self.__movimiento_lateral()
        else:
            self.__descenso()

        if current_time - self.ultimo_cambio_img > self.tiempo_cambio_img:
            self.posImg = (self.posImg + 1) % len(self.images)
            self.image = self.images[int(self.posImg)]
            self.ultimo_cambio_img = current_time

    def __movimiento_lateral(self):
        if self.derecha:
            self.rect.x += self.velocidad
            if self.rect.right > self.limiteder:
                self.derecha = False
                self.contador_mov_lateral += 1
        else:
            self.rect.x -= self.velocidad
            if self.rect.left < self.limiteizq:
                self.derecha = True
                self.contador_mov_lateral += 1

    def __descenso(self):
        if self.rect.y < self.max_descenso_actual:
            self.rect.y += 1
        else:
            self.contador_mov_lateral = 0
            self.max_descenso_actual = self.rect.y + DESPLAZAMIENTO_VERTICAL_ENEMIGO

    def atacar(self):
        if randint(0, 100) < self.rango_disparo:
            return Balon(self.rect.centerx, self.rect.bottom, IMAGEN_DISPARO_ENEMIGO, False)
        return None

class Balon(pygame.sprite.Sprite):
    def __init__(self, posx, posy, ruta_imagen, es_jugador):
        super().__init__()
        self.image = pygame.image.load(ruta_imagen).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = posx
        self.rect.centery = posy

        self.velocidad = VELOCIDAD_BALON_JUGADOR if es_jugador else VELOCIDAD_BALON_ENEMIGO
        self.es_disparo_jugador = es_jugador

    def update(self):
        if self.es_disparo_jugador:
            self.rect.y -= self.velocidad
        else:
            self.rect.y += self.velocidad

        if self.rect.bottom < 0 or self.rect.top > ALTO:
            self.kill()

# --- Funciones Auxiliares ---

def cargar_enemigos(enemy_group, all_sprites):
    # Limpiar grupos antes de cargar nuevos enemigos (útil al reiniciar el juego)
    enemy_group.empty()
    all_sprites.empty() # Asegúrate de no eliminar el jugador si ya está ahí

    pos_y_inicial_fila = 0
    for tipo_enemigo in ENEMIGO_TIPOS:
        posx_inicial = 100
        # Asegúrate de que las filas no se superpongan si 'y_offset' es pequeño
        # O simplemente usa una base fija para cada fila
        # Aquí usaremos el 'y_offset' directamente sumándole un valor base si fuera necesario
        # En tu diseño, 'y_offset' ya incluye esto, por lo que lo usamos directamente.
        
        for _ in range(4): # 4 enemigos por fila
            enemigo = noCreyente(posx_inicial, tipo_enemigo['y_offset'], 40,
                                 tipo_enemigo['img1'], tipo_enemigo['img2'], tipo_enemigo['puntos'])
            enemy_group.add(enemigo)
            all_sprites.add(enemigo)
            posx_inicial += 200 # Espacio entre enemigos

# --- Funciones de Puntuación ---

def cargar_puntuaciones():
    puntuaciones = []
    if os.path.exists(ARCHIVO_PUNTUACIONES):
        with open(ARCHIVO_PUNTUACIONES, 'r') as f:
            for line in f:
                try:
                    puntuaciones.append(int(line.strip()))
                except ValueError:
                    continue # Ignora líneas inválidas
    puntuaciones.sort(reverse=True) # Ordenar de mayor a menor
    return puntuaciones[:MAX_PUNTUaciones] # Devolver solo el top X

def guardar_puntuacion(nueva_puntuacion):
    puntuaciones = cargar_puntuaciones()
    puntuaciones.append(nueva_puntuacion)
    puntuaciones.sort(reverse=True)
    puntuaciones = puntuaciones[:MAX_PUNTUaciones] # Mantener solo el top X

    with open(ARCHIVO_PUNTUACIONES, 'w') as f:
        for score in puntuaciones:
            f.write(f"{score}\n")

# --- Funciones de Interfaz de Usuario ---

def dibujar_texto(superficie, texto, fuente, color, x, y):
    texto_superficie = fuente.render(texto, True, color)
    texto_rect = texto_superficie.get_rect()
    texto_rect.center = (x, y)
    superficie.blit(texto_superficie, texto_rect)

def dibujar_boton(superficie, rect, texto, fuente, color_normal, color_hover, mouse_pos):
    color_actual = color_normal
    if rect.collidepoint(mouse_pos):
        color_actual = color_hover
    pygame.draw.rect(superficie, color_actual, rect, border_radius=10) # Borde redondeado
    dibujar_texto(superficie, texto, fuente, NEGRO, rect.centerx, rect.centery)
    return rect.collidepoint(mouse_pos) # Retorna si el ratón está sobre el botón

# --- Pantallas del Juego ---

def mostrar_menu_principal(ventana, reloj):
    fuente_titulo = pygame.font.SysFont("Times New Roman", 70)
    fuente_boton = pygame.font.SysFont("Times New Roman", 40)

    # Definir rectángulos para los botones
    boton_jugar_rect = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 - 50, 200, 70)
    boton_puntuaciones_rect = pygame.Rect(ANCHO // 2 - 150, ALTO // 2 + 50, 300, 70)
    boton_salir_rect = pygame.Rect(ANCHO // 2 - 75, ALTO // 2 + 150, 150, 70) # Botón de salir

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if boton_jugar_rect.collidepoint(mouse_pos):
                    return "jugar"
                if boton_puntuaciones_rect.collidepoint(mouse_pos):
                    return "puntuaciones"
                if boton_salir_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        ventana.blit(pygame.image.load(IMAGEN_FONDO).convert(), (0, 0)) # Fondo del menú

        dibujar_texto(ventana, "BishoGame", fuente_titulo, BLANCO, ANCHO // 2, ALTO // 4)

        dibujar_boton(ventana, boton_jugar_rect, "Jugar", fuente_boton, AZUL_CLARO, GRIS_CLARO, mouse_pos)
        dibujar_boton(ventana, boton_puntuaciones_rect, "Puntuaciones Máximas", fuente_boton, AZUL_CLARO, GRIS_CLARO, mouse_pos)
        dibujar_boton(ventana, boton_salir_rect, "Salir", fuente_boton, AZUL_CLARO, GRIS_CLARO, mouse_pos)

        pygame.display.flip()
        reloj.tick(60)

def mostrar_puntuaciones_maximas(ventana, reloj):
    fuente_titulo = pygame.font.SysFont("Times New Roman", 60)
    fuente_puntuacion = pygame.font.SysFont("Times New Roman", 35)
    fuente_volver = pygame.font.SysFont("Times New Roman", 30)

    puntuaciones = cargar_puntuaciones()

    boton_volver_rect = pygame.Rect(ANCHO // 2 - 75, ALTO - 100, 150, 60)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if boton_volver_rect.collidepoint(mouse_pos):
                    return # Volver al menú principal

        ventana.blit(pygame.image.load(IMAGEN_FONDO).convert(), (0, 0))

        dibujar_texto(ventana, "Puntuaciones Máximas", fuente_titulo, BLANCO, ANCHO // 2, 80)

        y_offset = 180
        if not puntuaciones:
            dibujar_texto(ventana, "No hay puntuaciones aún.", fuente_puntuacion, BLANCO, ANCHO // 2, y_offset)
        else:
            for i, score in enumerate(puntuaciones):
                dibujar_texto(ventana, f"{i+1}. {score}", fuente_puntuacion, BLANCO, ANCHO // 2, y_offset + i * 40)

        dibujar_boton(ventana, boton_volver_rect, "Volver", fuente_volver, AZUL_CLARO, GRIS_CLARO, mouse_pos)

        pygame.display.flip()
        reloj.tick(60)

# --- Bucle Principal del Juego ---

def BishoGame():
    pygame.init()
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Bishogame")

    fondoimagen = pygame.image.load(IMAGEN_FONDO).convert()
    fuente_fin_juego = pygame.font.SysFont("Times New Roman", 50)
    fuente_puntuacion = pygame.font.SysFont("Times New Roman", 30)

    text_fin_juego = fuente_fin_juego.render("Fin del Juego", True, GRIS_OSCURO)

    reloj = pygame.time.Clock()

    estado_juego = "menu" # Estado inicial: "menu", "jugar", "puntuaciones"

    while True:
        if estado_juego == "menu":
            opcion_menu = mostrar_menu_principal(ventana, reloj)
            if opcion_menu == "jugar":
                estado_juego = "jugar"
            elif opcion_menu == "puntuaciones":
                estado_juego = "puntuaciones"
        elif estado_juego == "puntuaciones":
            mostrar_puntuaciones_maximas(ventana, reloj)
            estado_juego = "menu" # Volver al menú después de ver puntuaciones
        elif estado_juego == "jugar":
            # --- Configuración para un nuevo juego ---
            all_sprites = pygame.sprite.Group()
            player_group = pygame.sprite.Group()
            enemy_group = pygame.sprite.Group()
            player_bullets = pygame.sprite.Group()
            enemy_bullets = pygame.sprite.Group()

            jugador = BishoSiu()
            all_sprites.add(jugador)
            player_group.add(jugador)

            cargar_enemigos(enemy_group, all_sprites) # Asegura que los enemigos se recarguen

            puntuacion = 0
            en_juego = True
            
            # --- Bucle de juego activo ---
            while en_juego:
                current_time = pygame.time.get_ticks()
                reloj.tick(60)

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == K_LEFT:
                            jugador.movIzq()
                        elif event.key == K_RIGHT:
                            jugador.movDer()
                        elif event.key == K_c:
                            nuevo_balon = jugador.cabecear()
                            if nuevo_balon:
                                all_sprites.add(nuevo_balon)
                                player_bullets.add(nuevo_balon)

                # --- Actualización y Colisiones ---
                all_sprites.update(current_time)

                for enemigo in enemy_group:
                    disparo = enemigo.atacar()
                    if disparo:
                        all_sprites.add(disparo)
                        enemy_bullets.add(disparo)

                hits_player_bullet_enemy = pygame.sprite.groupcollide(enemy_group, player_bullets, True, True)
                for enemy_hit in hits_player_bullet_enemy:
                    puntuacion += enemy_hit.puntos

                hits_enemy_bullet_player = pygame.sprite.spritecollide(jugador, enemy_bullets, True)
                if hits_enemy_bullet_player:
                    jugador.destruir()
                    en_juego = False

                hits_enemy_player = pygame.sprite.spritecollide(jugador, enemy_group, False)
                if hits_enemy_player and jugador.vida:
                    jugador.destruir()
                    en_juego = False
                
                # Si todos los enemigos han sido destruidos, el jugador gana (puedes reiniciar nivel o ir al menú)
                if not enemy_group: # Si el grupo de enemigos está vacío
                    print("¡Todos los enemigos destruidos! ¡Has ganado!")
                    en_juego = False # Puedes cambiar esto para avanzar de nivel si lo deseas

                # --- Dibujado en juego ---
                ventana.blit(fondoimagen, (0, 0))
                all_sprites.draw(ventana)

                text_puntuacion = fuente_puntuacion.render(f"Puntos: {puntuacion}", True, VERDE_PUNTOS)
                ventana.blit(text_puntuacion, (10, 10))

                if not en_juego:
                    # Guardar puntuación si el juego termina
                    if jugador.vida: # Si el jugador ganó (destruyó a todos los enemigos)
                         guardar_puntuacion(puntuacion)
                         text_fin_juego = fuente_fin_juego.render("¡Victoria!", True, VERDE_PUNTOS) # Mensaje de victoria
                    else: # Si el jugador perdió
                         guardar_puntuacion(puntuacion) # Guardar puntuación aunque se pierda
                         text_fin_juego = fuente_fin_juego.render("Fin del Juego", True, GRIS_OSCURO) # Mensaje de game over
                    
                    ventana.blit(text_fin_juego, (ANCHO // 2 - text_fin_juego.get_width() // 2, ALTO // 2 - text_fin_juego.get_height() // 2))
                    pygame.display.update()
                    pygame.time.wait(2000) # Esperar 2 segundos antes de volver al menú
                    estado_juego = "menu" # Volver al menú principal

                pygame.display.update()

if __name__ == '__main__':
    BishoGame()
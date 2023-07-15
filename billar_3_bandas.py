import pygame
import random
import math

# Dimensiones de la mesa de billar
ANCHO = 800
ALTO = 400

# Colores
VERDE = (34, 139, 34)
MARRON = (139, 69, 19)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

# Físicas de las bolas
ROZAMIENTO = 0.98
VELOCIDAD_MAX = 5

class Bola:
    def __init__(self, x, y, color, masa):
        self.x = x
        self.y = y
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.color = color
        self.masa = masa

    def mover(self):
        self.x += self.velocidad_x
        self.y += self.velocidad_y

    def aplicar_rozamiento(self):
        self.velocidad_x *= ROZAMIENTO
        self.velocidad_y *= ROZAMIENTO

    def aplicar_limites_velocidad(self):
        if abs(self.velocidad_x) > VELOCIDAD_MAX:
            self.velocidad_x = VELOCIDAD_MAX if self.velocidad_x > 0 else -VELOCIDAD_MAX
        if abs(self.velocidad_y) > VELOCIDAD_MAX:
            self.velocidad_y = VELOCIDAD_MAX if self.velocidad_y > 0 else -VELOCIDAD_MAX

    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, self.color, (int(self.x), int(self.y)), 10)

    def colisionar(self, otra_bola):
        dx = otra_bola.x - self.x
        dy = otra_bola.y - self.y
        distancia = math.sqrt(dx ** 2 + dy ** 2)

        if distancia < 20:
            angulo = math.atan2(dy, dx)
            seno = math.sin(angulo)
            coseno = math.cos(angulo)

            # Rotación de las velocidades
            vx1 = self.velocidad_x * coseno + self.velocidad_y * seno
            vy1 = self.velocidad_y * coseno - self.velocidad_x * seno
            vx2 = otra_bola.velocidad_x * coseno + otra_bola.velocidad_y * seno
            vy2 = otra_bola.velocidad_y * coseno - otra_bola.velocidad_x * seno

            # Conservación del impulso
            velocidad_final_x1 = ((self.velocidad_x * (self.masa - otra_bola.masa)) + (2 * otra_bola.masa * otra_bola.velocidad_x)) / (self.masa + otra_bola.masa)
            velocidad_final_x2 = ((otra_bola.velocidad_x * (otra_bola.masa - self.masa)) + (2 * self.masa * self.velocidad_x)) / (self.masa + otra_bola.masa)

            # Asignación de las velocidades finales
            self.velocidad_x = velocidad_final_x1
            otra_bola.velocidad_x = velocidad_final_x2
            self.velocidad_y = vy1
            otra_bola.velocidad_y = vy2

    def aplicar_limites(self):
        if self.x < 120:
            self.x = 120
            self.velocidad_x *= -1
        elif self.x > 680:
            self.x = 680
            self.velocidad_x *= -1
        if self.y < 70:
            self.y = 70
            self.velocidad_y *= -1
        elif self.y > 330:
            self.y = 330
            self.velocidad_y *= -1

class Taco:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def golpear_bola(self, bola, cursor_x, cursor_y):
        diff_x = cursor_x - self.x
        diff_y = cursor_y - self.y
        distancia = math.sqrt(diff_x ** 2 + diff_y ** 2)

        if distancia > 0:
            unidad_x = diff_x / distancia
            unidad_y = diff_y / distancia

            bola.velocidad_x += unidad_x * 10
            bola.velocidad_y += unidad_y * 10

def dibujar_mesa():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Mesa de billar")

    reloj = pygame.time.Clock()
    terminado = False

    # Crear las bolas
    bola_blanca1 = Bola(400, 200, BLANCO, 1)
    bola_blanca2 = Bola(400, 220, BLANCO, 1)
    bola_roja = Bola(200, 200, ROJO, 2)

    bolas = [bola_blanca1, bola_blanca2, bola_roja]

    # Crear el taco
    taco = Taco(ANCHO // 2, ALTO // 2)

    bola_seleccionada = None

    while not terminado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                terminado = True
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  # Botón izquierdo del mouse presionado
                # Verificar si se hizo clic sobre alguna bola
                for bola in bolas:
                    distancia = math.sqrt((evento.pos[0] - bola.x) ** 2 + (evento.pos[1] - bola.y) ** 2)
                    if distancia <= 10:
                        bola_seleccionada = bola

            elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:  # Botón izquierdo del mouse liberado
                bola_seleccionada = None

        pantalla.fill(BLANCO)

        # Dibujar el exterior blanco
        pygame.draw.rect(pantalla, MARRON, (100, 50, 600, 300))

        # Dibujar las paredes internas invisibles del rectángulo verde
        pygame.draw.rect(pantalla, BLANCO, (110, 60, 10, 280))
        pygame.draw.rect(pantalla, BLANCO, (680, 60, 10, 280))
        pygame.draw.rect(pantalla, BLANCO, (110, 60, 580, 10))
        pygame.draw.rect(pantalla, BLANCO, (110, 330, 580, 10))

        # Dibujar la mesa de billar verde
        pygame.draw.rect(pantalla, VERDE, (120, 70, 560, 260))

        # Dibujar las bolas
        for bola in bolas:
            bola.dibujar(pantalla)

        # Obtener la posición del cursor del mouse
        cursor_x, cursor_y = pygame.mouse.get_pos()

        # Dibujar el taco
        pygame.draw.line(pantalla, BLANCO, (taco.x, taco.y), (cursor_x, cursor_y), 2)

        # Control del taco y golpear las bolas
        if pygame.mouse.get_pressed()[0] and bola_seleccionada is not None:  # Botón izquierdo del mouse presionado y hay una bola seleccionada
            taco.golpear_bola(bola_seleccionada, cursor_x, cursor_y)

        # Mover y aplicar límites a las bolas
        for bola in bolas:
            bola.mover()
            bola.aplicar_rozamiento()
            bola.aplicar_limites()

        # Colisionar con otras bolas
        for i in range(len(bolas)):
            for j in range(i + 1, len(bolas)):
                bola1 = bolas[i]
                bola2 = bolas[j]
                bola1.colisionar(bola2)

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()

# Llamar a la función para dibujar la mesa de billar
dibujar_mesa()

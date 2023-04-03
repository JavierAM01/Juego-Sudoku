import pygame
import os
import copy
from tableros import *


# Las coordenadas en pygame se expresan desde la esquina superior izquierda: 
# (x,y) --> x hacia la derecha, y hacia abajo  -->  el (0,0) es la esquina superior izquierda
ESTANTERIA = [board, hard, diff]

""" Variables Globales """
BORDE_X = 50
BORDE_Y = 70 
CAJA_X = CAJA_Y = 70
ALTURA = 9*CAJA_Y + 2*BORDE_Y 
ANCHURA = 9*CAJA_X + 2*BORDE_X 
FPS = 60 # frames per second
PANTALLA = pygame.display.set_mode((ANCHURA, ALTURA)) # PANTALLA_SUDOKU
pygame.display.set_caption("Sudoku. Creado por: Javier Abollado")  

""" coordenadas y dimensiones """
COORDENADA_CONTADOR = (BORDE_X + 3*CAJA_X, ALTURA - BORDE_Y + 10)
COORDENADA_RESOLVER = (ANCHURA//2 - 100, 5)
COORDENADA_END = (ANCHURA//2 - 250, 5)
DIMENSION_RESOLVER = (200, 70)
DIMENSION_TABLERO = (ANCHURA - 2*BORDE_X, ALTURA - 2*BORDE_Y)

""" colores en RGB """
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (100, 100, 100)




""" Definimos las clases cursor, para detectar donde apuntamos, boton para poder pulsar y hacer
acciones, y por último la clase Caja que guarda los 9x9 valores del Tablero """ 
class Cursor(pygame.Rect):

    def __init__(self):
        pygame.Rect.__init__(self, 0,0,1,1)

    def update(self):
        self.left, self.top = pygame.mouse.get_pos()

class Boton(pygame.sprite.Sprite): # sprite.Sprite

    def __init__(self, imagen, x, y):
        self.imagen = imagen
        self.rect = self.imagen.get_rect()
        self.rect.left, self.rect.top = (x, y)

    def actualizar(self):
        PANTALLA.blit(self.imagen, self.rect)

class Caja:

    def __init__(self, tablero, fila, columna):

        self.Tablero = tablero
        self.x = fila
        self.y = columna
        self.numero = tablero[fila][columna]
        self.temporal = 0
        self.coordenadas = (self.y*CAJA_X + BORDE_X, self.x*CAJA_Y + BORDE_Y)
        self.rectangulo = (self.coordenadas[0], self.coordenadas[1], CAJA_X, CAJA_Y)

    def introducir(self, numero):
        self.numero = numero
        self.temporal = 0
        self.Tablero[self.x][self.y] = numero

    def actualizar(self):

        self.numero = self.Tablero[self.x][self.y]

        if self.numero != 0:
            texto = str(self.numero)
            fuente = pygame.font.SysFont("Arial", 50)
            print_texto = fuente.render(texto, 0, NEGRO)
            coordenada_texto = self.coordenadas[0] + 26, self.coordenadas[1] + 8
            PANTALLA.blit(print_texto, coordenada_texto)

        elif self.temporal != 0:
            texto = str(self.temporal)
            fuente = pygame.font.SysFont("Arial", 30)
            print_texto = fuente.render(texto, 0, GRIS)
            coordenada_texto = self.coordenadas[0] + 5, self.coordenadas[1] + 5
            PANTALLA.blit(print_texto, coordenada_texto)


class Sudoku:


    """ funciones para resolver el sudoku: 'findEmpty' para encontrar huecos vacíos, 'es_valido' para 
    ver si se puede introducir el valor según los números del tablero actual y por último 'resolver' para 
    resolver el sudoku por completo"""
    def findEmpty(self, Tablero):
        for i in range(9):
            for j in range(9):
                if Tablero[i][j] == 0: return (i,j)
        return False

    def es_valido(self, Tablero, numero, x, y):

        # row
        for i in range(9):
            if Tablero[x][i] == numero and i != y: 
                return False

        # col
        for i in range(9):
            if Tablero[i][y] == numero and i != x: 
                return False

        # box
        bloque_x = x // 3
        bloque_y = y // 3
        for i in range(3*bloque_x, 3*bloque_x + 3):
            for j in range(3*bloque_y, 3*bloque_y + 3):
                if Tablero[i][j] == numero and (i,j) != (x,y): 
                    return False

        return True

    def resolver(self, Tablero):

        # find empty grid
        find = self.findEmpty(Tablero)
        if not find: return True
        x, y = find

        # fill valid
        for i in range(1,10):
            if self.es_valido(Tablero, i, x, y):
                Tablero[x][y] = i

                if self.resolver(Tablero): return True

                # undo
                Tablero[x][y] = 0

        return False



    """ acciones para crear nuestras variables iniciales """
    def descargar_imagen(self, nombre, escala):
        imagen = pygame.image.load(os.path.join("imagenes", nombre))
        return pygame.transform.scale(imagen, escala)

    def crear_cajas(self, tablero):
        cajas = {}
        for i in range(9):
            for j in range(9):
                cajas[str(i) + str(j)] = Caja(tablero, i, j)
        return cajas



    """ funciones para introducir números, borrarlos y comprobar si son válidos """ 
    def entrada_temporal(self, teclas_utilizadas, caja):

        # buscar tecla
        if teclas_utilizadas[pygame.K_1] or teclas_utilizadas[pygame.K_KP1]: numero = 1
        elif teclas_utilizadas[pygame.K_2] or teclas_utilizadas[pygame.K_KP2]: numero = 2
        elif teclas_utilizadas[pygame.K_3] or teclas_utilizadas[pygame.K_KP3]: numero = 3
        elif teclas_utilizadas[pygame.K_4] or teclas_utilizadas[pygame.K_KP4]: numero = 4
        elif teclas_utilizadas[pygame.K_5] or teclas_utilizadas[pygame.K_KP5]: numero = 5
        elif teclas_utilizadas[pygame.K_6] or teclas_utilizadas[pygame.K_KP6]: numero = 6
        elif teclas_utilizadas[pygame.K_7] or teclas_utilizadas[pygame.K_KP7]: numero = 7
        elif teclas_utilizadas[pygame.K_8] or teclas_utilizadas[pygame.K_KP8]: numero = 8
        elif teclas_utilizadas[pygame.K_9] or teclas_utilizadas[pygame.K_KP9]: numero = 9
        else: return

        caja.temporal = numero

    def analizar_entrada(self, tablero, caja, numero):

        if self.es_valido(tablero, numero, caja.x, caja.y):

            # introducimos
            caja.introducir(numero)
            copia = copy.deepcopy(tablero)
            copia[caja.x][caja.y] = numero
            if self.resolver(copia): 
                return True

            # undo
            caja.introducir(0)
            return False

        return False



    """ dibujar al final la pantalla y actualizarla """
    def dibujar_pantalla(self, cajas, imagen_fondo, tiempo, boton_resolver, boton_jugar, boton_endGamme, cursor, endGamme):

        PANTALLA.fill(BLANCO)
        PANTALLA.blit(imagen_fondo, (BORDE_X, BORDE_Y))   
        for caja in cajas: cajas[caja].actualizar()

        # tiempo
        segundos, minutos = tiempo % 60, tiempo // 60
        if segundos >= 10 and minutos >= 10:
            texto = f"Tiempo - {minutos}:{segundos}"
        if segundos < 10 and minutos >= 10:
            texto = f"Tiempo - {minutos}:0{segundos}"
        if segundos >= 10 and minutos < 10:
            texto = f"Tiempo - 0{minutos}:{segundos}"
        if segundos < 10 and minutos < 10:
            texto = f"Tiempo - 0{minutos}:0{segundos}"
        fuente = pygame.font.SysFont("Arial", 30)
        contador = fuente.render(texto, 0, NEGRO)
        PANTALLA.blit(contador, COORDENADA_CONTADOR)

        if not endGamme:
            # texto resolver
            boton_resolver.actualizar()
            fuente = pygame.font.SysFont("Arial", 30)
            print_texto = fuente.render("Resolver", 0, BLANCO)
            PANTALLA.blit(print_texto, (COORDENADA_RESOLVER[0] + 50, COORDENADA_RESOLVER[1] + 15))

        else: 
            # salir
            boton_endGamme.actualizar()
            fuente = pygame.font.SysFont("Arial", 30)
            print_texto = fuente.render("Salir", 0, BLANCO)
            PANTALLA.blit(print_texto, (COORDENADA_END[0] + 15 + 60, COORDENADA_END[1] + 15))
            # volver a jugar
            boton_jugar.actualizar()
            fuente = pygame.font.SysFont("Arial", 30)
            print_texto = fuente.render("Volver a jugar", 0, BLANCO)
            PANTALLA.blit(print_texto, (COORDENADA_END[0] + 20 + 300, COORDENADA_END[1] + 15))

        cursor.update()
        pygame.display.update() 

    # función principal
    def jugar(self, sudoku_seleccionado):
        # inicio
        pygame.init()
        cursor = Cursor()
        reloj = pygame.time.Clock() 
        # valores por defecto
        tiempo_aux = 0
        caja_seleccionada = 0
        run = True
        itereacion1 = True
        dif_tiempo = 0
        endGamme = False
        # objetos a utilizar
        TABLERO = copy.deepcopy(ESTANTERIA[sudoku_seleccionado])
        CAJAS = self.crear_cajas(TABLERO)
        fondo_boton = self.descargar_imagen("fondo_boton.png", DIMENSION_RESOLVER)
        fondo_sudoku = self.descargar_imagen("tablero_sudoku.png", DIMENSION_TABLERO)
        boton_resolver = Boton(fondo_boton, COORDENADA_RESOLVER[0], COORDENADA_RESOLVER[1])
        boton_endGamme = Boton(fondo_boton, COORDENADA_END[0], COORDENADA_END[1])
        boton_jugar = Boton(fondo_boton, COORDENADA_END[0] + 300, COORDENADA_END[1])
        while run:
            reloj.tick(FPS) 
            tiempo = pygame.time.get_ticks() // 1000
            if itereacion1:
                itereacion1 = False
                dif_tiempo = tiempo
            if tiempo_aux == tiempo - dif_tiempo: 
                tiempo_aux += 1
            teclas_utilizadas = pygame.key.get_pressed() 
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    # ver que caja hemos seleccionado
                    for caja in CAJAS:
                        if cursor.colliderect(CAJAS[caja].rectangulo):
                            caja_seleccionada = CAJAS[caja]
                    # boton resolver 
                    if cursor.colliderect(boton_resolver):
                        self.resolver(TABLERO)
                    # cuando terminamos el juego
                    if endGamme:
                        if cursor.colliderect(boton_endGamme):
                            return
                        elif cursor.colliderect(boton_jugar):
                            self.jugar(sudoku_seleccionado)
                            return                            
                if caja_seleccionada != 0:
                    self.entrada_temporal(teclas_utilizadas, caja_seleccionada)
                    # introducir numero definitivo
                    if teclas_utilizadas[pygame.K_RETURN] and caja_seleccionada.temporal != 0:
                        numero = caja_seleccionada.temporal
                        if self.analizar_entrada(TABLERO, caja_seleccionada, numero): pass 
                        else: caja_seleccionada.temporal = 0
                    # borrar numero temporal
                    if teclas_utilizadas[pygame.K_BACKSPACE] and caja_seleccionada.temporal != 0:
                        caja_seleccionada.temporal = 0 
            if not self.findEmpty(TABLERO): endGamme = True
            self.dibujar_pantalla(CAJAS, fondo_sudoku, tiempo_aux, boton_resolver, boton_jugar, boton_endGamme, cursor, endGamme) 
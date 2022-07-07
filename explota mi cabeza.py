import pygame, sys
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS
import random

# Pygame Variables
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

# tamaño de la ventana
ancho_ventana = 640
alto_ventana = 480

# asigna la variable pantalla y coloca el título de la ventana
pantalla = pygame.display.set_mode( (ancho_ventana, alto_ventana) )
pygame.display.set_caption('¡¡ Explota mi Cabeza !!')

# diccionario variables jugadores
j1 = {'dim_x': 80, 'dim_y': 100, # dimensiones cabeza jugador
      'pos_x': 175, 'pos_y': 275, # posiciones del jugador
      'letra_aleatoria': random.randint (0,3), # variable eleccion letra aleatoria jugador
      'puntos': 0
      }

j2 = {'dim_x': 80, 'dim_y': 100,
      'pos_x': 465, 'pos_y': 275,
      'letra_aleatoria': random.randint (0,3),
      'puntos': 0
      }

letras_j1 = ('A','S','D','W') # letras asignadas a jugador 1
teclas_j1 = (pygame.K_a,pygame.K_s,pygame.K_d,pygame.K_w) # teclas jugador 1

letras_j2 = ('O','P','K','L') # letras asignadas a jugador 2
teclas_j2 = (pygame.K_o,pygame.K_p,pygame.K_k,pygame.K_l)

dim_cuerpo = (120,180) # tamaño de los cuerpos

# definición de colores
rojo = 255,0,0
amarillo = 255, 255, 0
blanco = 255,255,255
verde = 50,140,10

# variables con las rutas de imágenes
imagenes = { 'boom_img': 'imagenes/bam.png',
             'fondo_avatar': 'imagenes/fondo_abstrac1_V2.jpg',
             'fondo_selector': 'imagenes/fondo_selector.jpg',
             'fondo_titulo': 'imagenes/fondo_titulo_v3.jpg',
             'fondo_ronda': 'imagenes/fondo_escenario_',
             'podium1': 'imagenes/podium1.png',
             'podium2': 'imagenes/podium2.png',
             'cuerpo': 'imagenes/cuerpo',
             'cabeza': 'imagenes/cabeza',
             'coco': 'imagenes/coco.png'
             }

# variables varias
aumento = 5 # incremento de la cabeza
avatar_posicion = ((150,210),(320,210),(490,210),(150,390),(320,390),(490,390)) # posicion avatares
cabeza_aleatoria = random.randint(1,6) # variable avatar aleatorio presentacion
coco_angulo = [45,360] # variable angulo rotacion cocos presentacion
modo_juego = 0 # elige la modalidad de juego

# diccionario con musicas de fondo
musica = {  'presentacion': 'sonidos/r0a-donkey-kong-country.mp3',
            'modo_juego': 'sonidos/r0b-mario-bros-2.mp3',
            'ronda': ('sonidos/r1-yoshis-island-1-yoshi.mp3',
                      'sonidos/r2-kirby-sand-canyon.mp3',
                      'sonidos/r3-donkey-kong-2-1.mp3'),
            'ganador': 'sonidos/r4-gta-san-andreas.mp3'
            }

# diccionario con sonidos
sonido = {  'inflar': pygame.mixer.Sound('sonidos/inflar.ogg'),
            'desinflar': pygame.mixer.Sound('sonidos/desinflar.ogg'),
            'explosion': pygame.mixer.Sound('sonidos/crash.ogg'),
            'cuenta_atras': pygame.mixer.Sound('sonidos/cuenta_atras.ogg')
            }

# diccionario record
record = { 'partidas_ganadas': [2,2,2,2,2,2],
           'avatar_pro': 0,
           'config_cargada': False
           }

# variables de control de flujo
empezar = False
hay_avatar = False
ronda = 1

#######################
###### funciones ######
#######################

# Leer y escribir el fichero de configuración de records
def leer_record():
    global record
    if record['config_cargada']:
        return
    
    # print ("estoy leyendo el config")
    try:
        fichero_record = open('record.txt', 'r')

        for puntos_avatar in range(0,6):
            record['partidas_ganadas'][puntos_avatar] = int( fichero_record.readline().rstrip() )

        fichero_record.close()
        record['config_cargada'] = True

    except:
        record = { 'partidas_ganadas': [2,2,2,2,2,2],
                   'avatar_pro': 0,
                   'config_cargada': False
                   }

def escribir_record():
    global record
    # print ("estoy grabando el config")
    
    fichero_record = open('record.txt', 'w')

    for puntos_avatar in range(0,6):
        fichero_record.write( str (record['partidas_ganadas'][puntos_avatar]) + "\n" )

    fichero_record.close()

# Cerrar ventana Salida del juego
def cerrar_ventana():
    for event in GAME_EVENTS.get():
        if event.type == GAME_GLOBALS.QUIT: 
            quitGame()

# Función salir del juego
def quitGame(): 
	pygame.quit()
	sys.exit()

# impresión de textos centrados
def imprime_texto_centrado(tamano,texto,color,pos_x,pos_y):
    fuente = pygame.font.Font(None, tamano)
    texto = fuente.render(texto, 0, color)
    ancho_texto = texto.get_width() # calcula el ancho del texto para centrarlo
    pantalla.blit(texto, (pos_x-(ancho_texto / 2),pos_y))

# muestra la letra que debe pulsar el jugador
def imprime_tecla(x_jugador,letras_jugador,pos_jugador): 
    texto = letras_jugador[x_jugador]
    imprime_texto_centrado(50,texto,blanco,pos_jugador+5,425)

# si acierta, incrementa cabeza
def acierto_tecla(x_jugador,dim_x,dim_y): 
    pygame.mixer.Sound.play(sonido['inflar'])
    dim_x += aumento
    dim_y += aumento*1.4
    x_jugador = letra_aleatoria(x_jugador)
    return x_jugador,dim_x,dim_y # la funcion retorna las variables de entrada modificadas

# elige otra letra
def letra_aleatoria(x_jugador): 
    x_jugador_old = x_jugador # controla que no repita la misma tecla dos veces seguidas
    while x_jugador == x_jugador_old:
        x_jugador = random.randint (0,3) # vuelve a elegir otra letra aleatoria
    return x_jugador # la funcion retorna las variables de entrada modificadas

# imprime la imagen centrada horizontal alineada abajo
def pon_imagen_centrada(fichero,dim_x,dim_y,pos_x,pos_y):
    imagen = pygame.image.load(fichero).convert_alpha()
    imagen = pygame.transform.scale (imagen,(dim_x,dim_y))
    pantalla.blit(imagen,(pos_x - (dim_x // 2), pos_y - dim_y))

# imprime la imagen a pantalla completa
def pon_imagen_pantalla_completa(imagen):
    fondo = pygame.image.load(imagen).convert_alpha()
    fondo = pygame.transform.scale (fondo,(ancho_ventana,alto_ventana))
    pantalla.blit(fondo,(0,0))

# dibuja la selección del avatar
def marcar_avatar(indice,texto,color): 
    pygame.draw.rect(pantalla, (color), (avatar_posicion[indice][0]-50, avatar_posicion[indice][1]-110, 100, 120), 5)
    pygame.draw.rect(pantalla, (color), (avatar_posicion[indice][0]-50, avatar_posicion[indice][1]+10, 100, 20), 0)
    
    imprime_texto_centrado(20,texto,blanco,avatar_posicion[indice][0],avatar_posicion[indice][1]+10)

# bucle elección de avatares
def elige_avatar(jugador):
    indice_avatar = 0
    if jugador == 2 and avatar_j1 == 0: # controla que el j2 empiece por avatar distinto a j1
        indice_avatar = 1
    
    while True: # pantalla elección avatar

        pon_imagen_pantalla_completa(imagenes['fondo_avatar'])

        # bucle para colocar los 6 avatares en pantalla
        contador_avatar = 1
        for avatar in avatar_posicion:
            pon_imagen_centrada(imagenes['cabeza']+str(contador_avatar)+'.png',80,100,avatar[0],avatar[1])

            texto = 'RECORD: '+str(record['partidas_ganadas'][contador_avatar-1])
            imprime_texto_centrado(16,texto,blanco,avatar[0],avatar[1]-125)
            
            contador_avatar += 1

        # selección del jugador 

        indice_mem = indice_avatar

        for event in GAME_EVENTS.get(): # comprueba pulsaciones de teclas
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if indice_avatar == 2: indice_avatar = 1
                    elif indice_avatar == 1: indice_avatar = 0
                    elif indice_avatar == 5: indice_avatar = 4
                    elif indice_avatar == 4: indice_avatar =3

                if event.key == pygame.K_RIGHT:
                    if indice_avatar == 0: indice_avatar = 1
                    elif indice_avatar == 1: indice_avatar = 2
                    elif indice_avatar == 3: indice_avatar = 4
                    elif indice_avatar == 4: indice_avatar = 5

                if event.key == pygame.K_UP:
                    if indice_avatar == 3: indice_avatar = 0
                    elif indice_avatar == 4: indice_avatar = 1
                    elif indice_avatar == 5: indice_avatar = 2

                if  event.key == pygame.K_DOWN:
                    if indice_avatar == 0: indice_avatar = 3
                    elif indice_avatar == 1: indice_avatar = 4
                    elif indice_avatar == 2: indice_avatar = 5

                if jugador == 2 and indice_avatar == avatar_j1: # evita seleccionar el mismo avatar
                    indice_avatar = indice_mem
            

                if event.key == pygame.K_SPACE:
                    return indice_avatar  

            if event.type == GAME_GLOBALS.QUIT: # Cerrar ventana Salida del juego
                quitGame()
            
            # permite seleccionar el avatar con el ratón
            posicion_raton = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0] == True:
                
                contador_avatar_raton = 0
                for avatar in avatar_posicion:
                    if posicion_raton[0] > avatar[0]-40 and posicion_raton[0] < avatar[0]+40:
                        if posicion_raton[1] > avatar[1]-100 and posicion_raton[1] < avatar[1]:
                            indice_avatar = contador_avatar_raton
                            if jugador == 2 and indice_avatar == avatar_j1: # evita seleccionar el mismo avatar
                                indice_avatar = indice_mem
                            elif jugador == 2 and indice_avatar != avatar_j1:
                                marcar_avatar(avatar_j1,'JUGADOR 1',rojo)
                                marcar_avatar(indice_avatar,'JUGADOR 2',verde)
                                pygame.display.update()
                                return indice_avatar
                            elif jugador == 1:
                                marcar_avatar(indice_avatar,'JUGADOR 1',rojo)
                                pygame.display.update()
                                return indice_avatar
                           
                    contador_avatar_raton += 1

        if jugador == 2:
            marcar_avatar(avatar_j1,'JUGADOR 1',rojo)
            marcar_avatar(indice_avatar,'JUGADOR 2',verde)
        else:
            marcar_avatar(indice_avatar,'JUGADOR 1',rojo)

        clock.tick(60)
        pygame.display.update()

# funcion animacion pantalla de titulo
def animacion_titulo(animacion_cabeza,cabeza_aleatoria):
    global coco_angulo , empezar

    pon_imagen_pantalla_completa(imagenes['fondo_titulo'])
        
    pon_imagen_centrada(imagenes['cuerpo']+str(cabeza_aleatoria)+'.png',dim_cuerpo[0],dim_cuerpo[1],j1['pos_x']-50,145+j1['pos_y'])
    pon_imagen_centrada(imagenes['cabeza']+str(cabeza_aleatoria)+'.png',(j1['dim_x']+animacion_cabeza),(j1['dim_y']+(animacion_cabeza*1.4)),j1['pos_x']-50,j1['pos_y'])

    # animación del giro de los cocos
    coco_1 = pygame.image.load(imagenes['coco']).convert_alpha()
    coco_1 = pygame.transform.scale (coco_1,(56,56))
    coco_1 = pygame.transform.rotate (coco_1,coco_angulo[0])
    coco_angulo[0] += 4
    ancho_coco = coco_1.get_width() # calcula ancho de la imagen después de rotar
    alto_coco = coco_1.get_height() # para calcular el centro y que no descentre la animación
    if coco_angulo[0] > 360: coco_angulo[0] = 0
    pantalla.blit(coco_1,(370-(ancho_coco/2),388-(alto_coco/2)))

    coco_2 = pygame.image.load(imagenes['coco']).convert_alpha()
    coco_2 = pygame.transform.scale (coco_2,(56,56))
    coco_2 = pygame.transform.rotate (coco_2,coco_angulo[1])
    coco_angulo[1] -= 4
    ancho_coco_2 = coco_2.get_width()
    alto_coco_2 = coco_2.get_height()
    if coco_angulo[1] < 0: coco_angulo[1] = 359
    pantalla.blit(coco_2,(470-(ancho_coco_2/2),388-(alto_coco_2/2)))

    # calcula y pon el avatar que tiene mas partidas ganadas
    record['avatar_pro'] = record['partidas_ganadas'].index(max(record['partidas_ganadas']))
    pon_imagen_centrada(imagenes['cuerpo']+str(record['avatar_pro']+1)+'.png',dim_cuerpo[0]-55,dim_cuerpo[1]-55,j1['pos_x']+385,150+j1['pos_y'])
    pon_imagen_centrada(imagenes['cabeza']+str(record['avatar_pro']+1)+'b.png',(j1['dim_x']-15),(j1['dim_y']-15),j1['pos_x']+385,48+j1['pos_y'])

    texto = str(max(record['partidas_ganadas']))
    imprime_texto_centrado(32,texto,blanco,393,282)

    for event in GAME_EVENTS.get(): # comprueba pulsaciones de espacio
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                empezar = True
        if event.type == GAME_GLOBALS.QUIT: # Cerrar ventana Salida del juego
            quitGame()

        # comprueba si se hace clic con el ratón
        if pygame.mouse.get_pressed()[0] == True:
            empezar = True

    clock.tick(60)
    pygame.display.update()

# bucle principal de la pantalla de título
def bucle_titulo():
    global cabeza_aleatoria
    cabeza_aleatoria_old = cabeza_aleatoria
    while cabeza_aleatoria == cabeza_aleatoria_old: # controla que no repita el mismo avatar seguido
        cabeza_aleatoria = random.randint(1,6)
    
    for animacion_cabeza in range(0,100,4):
        animacion_titulo(animacion_cabeza,cabeza_aleatoria)
        if empezar == True:
            return

    for animacion_cabeza in range(100,0,-4):
        animacion_titulo(animacion_cabeza,cabeza_aleatoria)
        if empezar == True:
            return

# rutina cuenta atrás inicio ronda
def cuenta_atras():
    pygame.mixer.music.stop() # para la música de fondo
    pygame.mixer.Sound.play(sonido['cuenta_atras'])
    
    for contador in ('3','2','1','GO!'):

        imagen = imagenes['fondo_ronda']+str(ronda)+'.jpg'
        pon_imagen_pantalla_completa(imagen)

        dibuja_jugadores()
 
        imprime_texto_centrado(120,contador,amarillo,ancho_ventana/2,230)

        texto = 'Gana el primero que haga 2 rondas'
        imprime_texto_centrado(30,texto,amarillo,ancho_ventana/2,80)

        imprime_puntuacion()
        
        cerrar_ventana()
        pygame.display.update()
        clock.tick(1)

# imprime la puntuación de la partida
def imprime_puntuacion():
    texto = str(j1['puntos'])+'-'+str(j2['puntos'])
    imprime_texto_centrado(80,texto,amarillo,ancho_ventana/2,120)

# dibuja jugadores
def dibuja_jugadores():
    # dibuja_jugador 1
    pon_imagen_centrada(imagenes['cuerpo']+str(avatar_j1+1)+'.png',dim_cuerpo[0],dim_cuerpo[1],j1['pos_x'],145+j1['pos_y'])
    pon_imagen_centrada(imagenes['cabeza']+str(avatar_j1+1)+'.png',j1['dim_x'],j1['dim_y'],j1['pos_x'],j1['pos_y'])

    # dibuja_jugador 2
    pon_imagen_centrada(imagenes['cuerpo']+str(avatar_j2+1)+'.png',dim_cuerpo[0],dim_cuerpo[1],j2['pos_x'],145+j2['pos_y'])
    pon_imagen_centrada(imagenes['cabeza']+str(avatar_j2+1)+'.png',j2['dim_x'],j2['dim_y'],j2['pos_x'],j2['pos_y'])

# bucle principal de las rondas de juego
def bucle_ronda():
    global j1 , j2
    while (j1['dim_x'] < 180) and (j2['dim_x'] < 180):
    
        for event in GAME_EVENTS.get(): # comprueba pulsaciones de teclas
            if event.type == pygame.KEYDOWN:
                # jugador 1
                for tecla in teclas_j1: # comprueba que coinciden tecla y letra en las listas
                    if event.key == tecla and j1['letra_aleatoria'] != teclas_j1.index(tecla): # control antispam
                        if j1['dim_x'] > 80: # tamaño mínimo
                            pygame.mixer.Sound.play(sonido['desinflar'])
                            j1['dim_x'] -= aumento
                            j1['dim_y'] -= aumento*1.4
                    elif event.key == tecla and j1['letra_aleatoria'] == teclas_j1.index(tecla):
                        j1['letra_aleatoria'],j1['dim_x'],j1['dim_y'] = acierto_tecla(j1['letra_aleatoria'],j1['dim_x'],j1['dim_y'])
                        if modo_juego == 2:
                            j2['letra_aleatoria'] = letra_aleatoria(j2['letra_aleatoria'])

                # jugador 2
                for tecla in teclas_j2: # comprueba que coinciden tecla y letra en las listas
                    if event.key == tecla and j2['letra_aleatoria'] != teclas_j2.index(tecla): # control antispam
                        if j2['dim_x'] > 80: # tamaño mínimo
                            pygame.mixer.Sound.play(sonido['desinflar'])
                            j2['dim_x'] -= aumento
                            j2['dim_y'] -= aumento*1.4
                    elif event.key == tecla and j2['letra_aleatoria'] == teclas_j2.index(tecla):   
                        j2['letra_aleatoria'],j2['dim_x'],j2['dim_y'] = acierto_tecla(j2['letra_aleatoria'],j2['dim_x'],j2['dim_y'])
                        if modo_juego == 2:
                            j1['letra_aleatoria'] = letra_aleatoria(j1['letra_aleatoria'])
                            
                if event.key == pygame.K_ESCAPE: # Tecla ESC Salida del juego
                    quitGame()

            if event.type == GAME_GLOBALS.QUIT: # Cerrar ventana Salida del juego
                quitGame()

        imagen = imagenes['fondo_ronda']+str(ronda)+'.jpg'
        pon_imagen_pantalla_completa(imagen)

        dibuja_jugadores()
        
        imprime_tecla(j1['letra_aleatoria'],letras_j1,j1['pos_x']) # dibuja letra jugador 1
        imprime_tecla(j2['letra_aleatoria'],letras_j2,j2['pos_x']) # dibuja letra jugador 2

        imprime_ronda()

        imprime_puntuacion()
        
        clock.tick(60)
        pygame.display.update()

# imprime la ronda actual
def imprime_ronda():
    texto = 'Ronda '+str(ronda)
    imprime_texto_centrado(45,texto,amarillo,ancho_ventana/2,80)

# rutina para esperar que se pulse espacion para continuar
def pulsa_espacio():
    texto = 'Pulsa ESPACIO'
    imprime_texto_centrado(25,texto,blanco,ancho_ventana/2,340)

    texto = 'para continuar'
    imprime_texto_centrado(25,texto,blanco,ancho_ventana/2,360)
    
    pygame.display.update()
    
    espera = False
    while espera == False:
        for event in GAME_EVENTS.get(): # comprueba pulsación de espacio
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    espera = True

            # comprueba si se hace clic con el ratón
            if pygame.mouse.get_pressed()[0] == True:
                espera = True

            if event.type == GAME_GLOBALS.QUIT: # Cerrar ventana Salida del juego
                quitGame()

        cerrar_ventana()
        clock.tick(60)

# muestra la explosión al ganar la ronda
def explosion():
    global j1 , j2
    pygame.mixer.music.stop() # para la música de fondo
    pygame.mixer.Sound.play(sonido['explosion'])
    
    if j1['dim_x'] > j2['dim_x']:
        imagen = pygame.image.load(imagenes['boom_img']).convert_alpha()
        imagen = pygame.transform.scale (imagen,(400,350))
        pantalla.blit(imagen,(j1['pos_x'] - (400 // 2), -40))
        j1['puntos'] += 1

    else:
        imagen = pygame.image.load(imagenes['boom_img']).convert_alpha()
        imagen = pygame.transform.scale (imagen,(400,350))
        pantalla.blit(imagen,(j2['pos_x'] - (400 // 2), -40))
        j2['puntos'] += 1

    imprime_ronda()
    imprime_puntuacion()
    pulsa_espacio()

# rutina para la pantalla de ganador
def pantalla_ganador():
    global j1 , j2 , record

    imagen = imagenes['fondo_ronda']+str(ronda)+'.jpg'
    pon_imagen_pantalla_completa(imagen)
        
    if j1['puntos'] > j2['puntos']:
        pon_imagen_pantalla_completa(imagenes['podium1'])
            
        pon_imagen_centrada(imagenes['cuerpo']+str(avatar_j1+1)+'.png',dim_cuerpo[0],dim_cuerpo[1],j1['pos_x'],145+j1['pos_y']-15)
        pon_imagen_centrada(imagenes['cabeza']+str(avatar_j1+1)+'b.png',150,198,j1['pos_x'],j1['pos_y']-15)

        pon_imagen_centrada(imagenes['cuerpo']+str(avatar_j2+1)+'.png',dim_cuerpo[0],dim_cuerpo[1],j2['pos_x'],145+j2['pos_y']+15)
        pon_imagen_centrada(imagenes['cabeza']+str(avatar_j2+1)+'c.png',150,198,j2['pos_x'],j2['pos_y']+15)

        imprime_ganador(1)
        record['partidas_ganadas'][avatar_j1] += 1

    else:
        pon_imagen_pantalla_completa(imagenes['podium2'])
            
        pon_imagen_centrada(imagenes['cuerpo']+str(avatar_j1+1)+'.png',dim_cuerpo[0],dim_cuerpo[1],j1['pos_x'],145+j1['pos_y']+15)
        pon_imagen_centrada(imagenes['cabeza']+str(avatar_j1+1)+'c.png',150,198,j1['pos_x'],j1['pos_y']+15)

        pon_imagen_centrada(imagenes['cuerpo']+str(avatar_j2+1)+'.png',dim_cuerpo[0],dim_cuerpo[1],j2['pos_x'],145+j2['pos_y']-15)
        pon_imagen_centrada(imagenes['cabeza']+str(avatar_j2+1)+'b.png',150,198,j2['pos_x'],j2['pos_y']-15)

        imprime_ganador(2)
        record['partidas_ganadas'][avatar_j2] += 1

    escribir_record()

    pulsa_espacio()

# imprime el texto el jugador que ha ganado
def imprime_ganador(jugador):

    texto = 'GANADOR'
    imprime_texto_centrado(35,texto,amarillo,ancho_ventana/2,210)

    texto = 'JUGADOR'
    imprime_texto_centrado(45,texto,amarillo,ancho_ventana/2,240)

    texto = str(jugador)
    imprime_texto_centrado(90,texto,amarillo,ancho_ventana/2,270)

# pantalla de selección de modo de juego
def selector_modo():
    global modo_juego

    pon_imagen_pantalla_completa(imagenes['fondo_selector'])

    pygame.display.update()

    while modo_juego == 0:
        for event in GAME_EVENTS.get(): # comprueba pulsaciones de teclas
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    modo_juego =1
                if event.key == pygame.K_2:
                    modo_juego =2
            if event.type == GAME_GLOBALS.QUIT: # Cerrar ventana Salida del juego
                quitGame()

            # permite seleccionar el modo con el ratón
            posicion_raton = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0] == True:
                
                if posicion_raton[0] > 80 and posicion_raton[0] < 260:
                    if posicion_raton[1] > 315 and posicion_raton[1] < 390:
                        modo_juego = 1
                if posicion_raton[0] > 380 and posicion_raton[0] < 560:
                    if posicion_raton[1] > 315 and posicion_raton[1] < 390:
                        modo_juego = 2
            
        cerrar_ventana()
        clock.tick(60)

# poner música en bucle
def pon_musica(fichero,volumen):
    pygame.mixer.music.load(fichero)
    pygame.mixer.music.set_volume(volumen)
    pygame.mixer.music.play(-1)

# bucle principal del juego

while True:
    pon_musica(musica['presentacion'],0.5)

    while empezar == False: # llama a la pantalla de animacion del de titulo

        leer_record()
        bucle_titulo()

    if modo_juego == 0:  # llama al selector de modo de juego
        pon_musica(musica['modo_juego'],0.5)
        
        selector_modo()

    if hay_avatar == False:  # llama a la rutina elegir avatar
        avatar_j1 = elige_avatar(1)
        avatar_j2 = elige_avatar(2)
        clock.tick(1)
        hay_avatar = True

    if hay_avatar == True: # comienza la cuenta atras y las rondas

        cuenta_atras()

        pon_musica(musica['ronda'][ronda-1],0.6) # pone la música según la ronda que sea

        bucle_ronda()
        
        explosion()   # al volver del bucle ronda pinta la explosión y reinicia tamaños
        j1['dim_x'] = 80
        j1['dim_y'] = 100
        j2['dim_x'] = 80
        j2['dim_y'] = 100
        if ronda < 3: ronda += 1
                
        if j1['puntos'] == 2 or j2['puntos'] == 2:  # comprueba si hay que ir a la pantalla ganador

            pon_musica(musica['ganador'],0.5)
        
            pantalla_ganador()

            j1['puntos'] = 0  # reinicia variables para volver a la pantalla de inicio
            j2['puntos'] = 0
            empezar = False
            hay_avatar = False
            ronda = 1
            modo_juego = 0

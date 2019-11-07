# Libreria math para funciones de cos y sin
import math
# Libreria csv para leer el archivo de datos
import csv
# Librerias de openGL
from OpenGL.GL import *
from OpenGL.GLUT import *  # GL Utilities Toolkit
from OpenGL.GLU import *
import square_module
import random

width = 800
height = 600
tempX = 0
tempY = 0
board_squares = list()
dragging = False
ESCAPE = as_8_bit('\033')
auxiliar_shape = square_module.Shape(list())
shape_index = None
init = True
game_shapes = list()
elegible_shapes = list()
matriz = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
point_size = 50
shape_actual = None
lose = False
score = 0


def printText(font, string): #Escribe el texto en pantalla
    for c in string:
        glutBitmapCharacter(font, ctypes.c_int(ord(c)))


def print_score(): #Escribe el score del jugador en pantalla
    glColor3f(0.0, 0.0, 0.0)
    glRasterPos3f(-350, 280, 0.0)
    printText(GLUT_BITMAP_HELVETICA_18, "Score: "+str(score))


def print_lose(): #Escribe si el jugador perdio en pantalla
    glColor3f(0.0, 0.0, 0.0)
    glRasterPos3f(-250, 280, 0.0)
    printText(GLUT_BITMAP_HELVETICA_18, "Perdiste!")


def draw_matrix():
    glColor3f(1.0, 0.0, 0.0)
    for f in range(11):
        for c in range(11):
            if matriz[f][c] == 1:
                glPointSize(point_size)
                glBegin(GL_POINTS)
                glVertex2f((f*50)-350, (c*50)-250)
                glEnd()


def validate_line():
    global score
    cont = 0
    for f in range(11):
        for c in range(11):
            if matriz[f][c] == 1:
                cont += 1
        if cont == 11:
            score += 100
            print_score()
            for c in range(11):
                matriz[f][c] = 0
        cont = 0
    cont = 0
    for f in range(11):
        for c in range(11):
            if matriz[c][f] == 1:
                cont += 1
        if cont == 11:
            score += 100
            print_score()
            for c in range(11):
                matriz[c][f] = 0
        cont = 0


def test_actual_shapes():
    global lose
    fc = 0
    for shape in elegible_shapes:
        for f in range(11):
            for c in range(11):
                if matriz[f][c] == 0:
                    if valid_shapes((f*50)-350, (c*50)-250, shape.get_type()):
                        fc += 1
    if fc == 0:
        lose = True


def generate_board(): #Genera los cuadros del tablero de 10x10
    global board_squares
    y = 1
    x = 1

    for count in range(11):
        x = 1
        for count2 in range(11):
            sq = square_module.Square(-400 + (50*x), -300 + (50*y), 0)
            board_squares.append(sq)
            x += 1
        y += 1


def move_figure(): #Actualiza las coordenadas x,y de la figura seleccionada
    game_shapes[shape_index].set_midpoint_xy(tempX, tempY)


def drawSlider():  # Dibuja el area donde se dibujaran las piezas elegibles para el jugador
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_POLYGON)
    glVertex2d(200, 300)  # Superior izquierda
    glVertex2d(200, -300)  # Inferior izquierda
    glVertex2d(400, -300)  # Inferior derecha
    glVertex2d(400, 300)  # Superior derecha
    glEnd()


# OpenGL functions
def printInteraction():
    print("Elaborado por:")
    print("Raul Balleza, Carlos Daniel, Roman Vazquez, Marisol Izaguirre")
    print("Wood Block Game")
    print("ESC - Salir del juego")
    print("Arrastra con tu mouse los bloques de la izquierda hacia el area de la derecha")
    print("Completa una fila para obtener puntos")
    print("Elige bien tus piezas para tener suficiente espacio en el tablero")


def init():
    # red, green, blue, alpha from 0.0 to 1.0
    glClearColor(1.0, 1.0, 1.0, 0.0)
    generate_board()
    set_elegible_shapes(3)


def resize(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Set viewing box dimensions equal to window dimensions.
    glOrtho(-w/2, w/2, -h/2, h/2, -1.0, 1.0)

    # Pass the size of the OpenGL window to globals.
    width = w
    height = h

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyInput(key, x, y):
    # Si la tecla presionada es el ESCAPE entonces el programa finaliza
    if key == ESCAPE:
        sys.exit()


def set_elegible_shapes(number):
    #Recibe un el numero de figuras random a generar y la agrega a las figuras seleccionables para el usuario
    for count in range(number):
        #Segun el numero generado, clona una figura del arreglo de figuras en general a el arreglo de figuras elegibles
        aux_shape = square_module.shapes[random.randint(
            0, len(square_module.shapes)-1)]
        shape = square_module.Shape(aux_shape.get_points())
        shape.set_type(aux_shape.get_type())
        elegible_shapes.append(shape)


def draw_elegible_shapes():
    #Dibuja las figuras seleccionables para el usuario en el area del slider
    y = -200
    for shape in elegible_shapes:
        glColor3ub(255, 0, 0)
        shape.set_midpoint_xy(300, y)
        shape.draw_shape(shape.get_midpoint_x(), shape.get_midpoint_y())
        y += 200


def draw_game_shapes():
    #Dibuja las figuras que han sido seleccionadas y puestas en el tablero
    for shape in game_shapes:
        glColor3ub(255, 0, 0)
        shape.draw_shape(shape.get_midpoint_x(), shape.get_midpoint_y())


def draw_board(): #Dibuja el tablero
    for square in board_squares:
        square.draw_square()


def displayMe():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    drawSlider()
    draw_board()
    draw_elegible_shapes()
    if dragging:
        move_figure()
    draw_game_shapes()
    draw_matrix()
    print_score()
    if lose:
        print_lose()
    glutSwapBuffers()


def check_figure(x, y): #Checa si el click que dio el usuario es coincide dentro del area de una figura para poder agarrarla
    global shape_index
    global elegible_shapes
    global game_shapes
    global shape_actual
    shape_index = None
    for shape in elegible_shapes:
        if shape.in_range(x, y):
            shape_actual = shape
            elegible_shapes.remove(shape)
            game_shapes.append(shape)
            shape_index = game_shapes.index(shape)
            global dragging #Variable para saber si esta arreastrando una pieza o no
            dragging = True


def passive_mouse_control(x, y): #Actualiza las coordenadas que se le daran a la figura seleccionada
    global tempX #Coordenada en x del mouse
    tempX = -width / 2 + width * x / width
    global tempY #Coordenada en y del mouse
    tempY = height / 2 - height * y / height
    glutPostRedisplay()


def valid_shapes(vX, vY, typeS):
    validX = False
    validY = False
    valid = False
    validP = False
    valueX = None
    valueY = None
    for val in range(-350, 150+1, 50):
        if(vX >= val-20 and vX <= val+20):
            validX = True
            valueX = val

    for val in range(-250, 250+1, 50):
        if(vY >= val-20 and vY <= val+20):
            validY = True
            valueY = val

    if(validX and validY):
        #valid = True
        if typeS == 1:
            if(valueX >= -300 and valueX <= 100 and valueY >= -200 and valueY <= 200):
                valid = True
        if typeS == 2:
            if(valueX >= -300 and valueX <= 100 and valueY >= -200 and valueY <= 200):
                valid = True
        if typeS == 3:
            if(valueX >= -350 and valueX <= 100 and valueY >= -200 and valueY <= 200):
                valid = True
        if typeS == 4:
            if(valueX >= -350 and valueX <= 100 and valueY >= -200 and valueY <= 200):
                valid = True
        if typeS == 5:
            if(valueX >= -300 and valueX <= 150 and valueY >= -200 and valueY <= 250):
                valid = True
        if typeS == 6:
            if(valueX >= -350 and valueX <= 150 and valueY >= -250 and valueY <= 250):
                valid = True
        if typeS == 7:
            if(valueX >= -300 and valueX <= 100 and valueY >= -250 and valueY <= 250):
                valid = True
        if typeS == 8:
            if(valueX >= -350 and valueX <= 150 and valueY >= -200 and valueY <= 200):
                valid = True
        if valid:
            if typeS == 1:
                pos1x = int((valueX-50+350)/50)
                pos1y = int((valueY+50+250)/50)

                pos2x = int((valueX+350)/50)
                pos2y = int((valueY+50+250)/50)

                pos3x = int((valueX+50+350)/50)
                pos3y = int((valueY+50+250)/50)

                pos4x = int((valueX+50+350)/50)
                pos4y = int((valueY+250)/50)

                pos5x = int((valueX+50+350)/50)
                pos5y = int((valueY-50+250)/50)
                if(matriz[pos1x][pos1y] == 0 and matriz[pos2x][pos2y] == 0 and matriz[pos3x][pos3y] == 0 and
                   matriz[pos4x][pos4y] == 0 and matriz[pos5x][pos5y] == 0):
                    validP = True
            if typeS == 2:
                pos1x = int((valueX-50+350)/50)
                pos1y = int((valueY+50+250)/50)

                pos2x = int((valueX+350)/50)
                pos2y = int((valueY+50+250)/50)

                pos3x = int((valueX+50+350)/50)
                pos3y = int((valueY+50+250)/50)

                pos4x = int((valueX-50+350)/50)
                pos4y = int((valueY+250)/50)

                pos5x = int((valueX-50+350)/50)
                pos5y = int((valueY-50+250)/50)
                if(matriz[pos1x][pos1y] == 0 and matriz[pos2x][pos2y] == 0 and matriz[pos3x][pos3y] == 0 and
                   matriz[pos4x][pos4y] == 0 and matriz[pos5x][pos5y] == 0):
                    validP = True
            if typeS == 3:
                pos1x = int((valueX+350)/50)
                pos1y = int((valueY+50+250)/50)

                pos2x = int((valueX+50+350)/50)
                pos2y = int((valueY+50+250)/50)

                pos3x = int((valueX+50+350)/50)
                pos3y = int((valueY+250)/50)

                pos4x = int((valueX+50+350)/50)
                pos4y = int((valueY-50+250)/50)
                if(matriz[pos1x][pos1y] == 0 and matriz[pos2x][pos2y] == 0 and matriz[pos3x][pos3y] == 0 and
                   matriz[pos4x][pos4y] == 0):
                    validP = True
            if typeS == 4:
                pos1x = int((valueX+50+350)/50)
                pos1y = int((valueY+50+250)/50)

                pos2x = int((valueX+50+350)/50)
                pos2y = int((valueY+250)/50)

                pos3x = int((valueX+50+350)/50)
                pos3y = int((valueY-50+250)/50)

                pos4x = int((valueX+350)/50)
                pos4y = int((valueY-50+250)/50)
                if(matriz[pos1x][pos1y] == 0 and matriz[pos2x][pos2y] == 0 and matriz[pos3x][pos3y] == 0 and
                   matriz[pos4x][pos4y] == 0):
                    validP = True
            if typeS == 5:
                pos1x = int((valueX+350)/50)
                pos1y = int((valueY+250)/50)

                pos2x = int((valueX-50+350)/50)
                pos2y = int((valueY+250)/50)

                pos3x = int((valueX-50+350)/50)
                pos3y = int((valueY-50+250)/50)

                pos4x = int((valueX+350)/50)
                pos4y = int((valueY-50+250)/50)
                if(matriz[pos1x][pos1y] == 0 and matriz[pos2x][pos2y] == 0 and matriz[pos3x][pos3y] == 0 and
                   matriz[pos4x][pos4y] == 0):
                    validP = True
            if typeS == 6:
                pos1x = int((valueX+350)/50)
                pos1y = int((valueY+250)/50)
                if(matriz[pos1x][pos1y] == 0):
                    validP = True
            if typeS == 7:
                pos1x = int((valueX-50+350)/50)
                pos1y = int((valueY+250)/50)

                pos2x = int((valueX+350)/50)
                pos2y = int((valueY+250)/50)

                pos3x = int((valueX+50+350)/50)
                pos3y = int((valueY+250)/50)
                if(matriz[pos1x][pos1y] == 0 and matriz[pos2x][pos2y] == 0 and matriz[pos3x][pos3y] == 0):
                    validP = True
            if typeS == 8:
                pos1x = int((valueX+350)/50)
                pos1y = int((valueY+50+250)/50)

                pos2x = int((valueX+350)/50)
                pos2y = int((valueY+250)/50)

                pos3x = int((valueX+350)/50)
                pos3y = int((valueY-50+250)/50)
                if(matriz[pos1x][pos1y] == 0 and matriz[pos2x][pos2y] == 0 and matriz[pos3x][pos3y] == 0):
                    validP = True
            if validP:
                return True
    return False


def valid_movement():
    #-350 -250
    # 150 250
    global tempX
    global tempY
    global dragging
    validX = False
    validY = False
    valid = False
    validP = False
    valueX = None
    valueY = None
    for val in range(-350, 150+1, 50):
        if(tempX >= val-20 and tempX <= val+20):
            validX = True
            valueX = val

    for val in range(-250, 250+1, 50):
        if(tempY >= val-20 and tempY <= val+20):
            validY = True
            valueY = val

    if(validX and validY):
        #valid = True
        if shape_actual.get_type() == 1:
            if(valueX >= -300 and valueX <= 100 and valueY >= -200 and valueY <= 200):
                valid = True
        if shape_actual.get_type() == 2:
            if(valueX >= -300 and valueX <= 100 and valueY >= -200 and valueY <= 200):
                valid = True
        if shape_actual.get_type() == 3:
            if(valueX >= -350 and valueX <= 100 and valueY >= -200 and valueY <= 200):
                valid = True
        if shape_actual.get_type() == 4:
            if(valueX >= -350 and valueX <= 100 and valueY >= -200 and valueY <= 200):
                valid = True
        if shape_actual.get_type() == 5:
            if(valueX >= -300 and valueX <= 150 and valueY >= -200 and valueY <= 250):
                valid = True
        if shape_actual.get_type() == 6:
            if(valueX >= -350 and valueX <= 150 and valueY >= -250 and valueY <= 250):
                valid = True
        if shape_actual.get_type() == 7:
            if(valueX >= -300 and valueX <= 100 and valueY >= -250 and valueY <= 250):
                valid = True
        if shape_actual.get_type() == 8:
            if(valueX >= -350 and valueX <= 150 and valueY >= -200 and valueY <= 200):
                valid = True
        if valid:
            if shape_actual.get_type() == 1:
                pos1x = int((valueX-50+350)/50)
                pos1y = int((valueY+50+250)/50)

                pos2x = int((valueX+350)/50)
                pos2y = int((valueY+50+250)/50)

                pos3x = int((valueX+50+350)/50)
                pos3y = int((valueY+50+250)/50)

                pos4x = int((valueX+50+350)/50)
                pos4y = int((valueY+250)/50)

                pos5x = int((valueX+50+350)/50)
                pos5y = int((valueY-50+250)/50)
                if(matriz[pos1x][pos1y] == 0 and matriz[pos2x][pos2y] == 0 and matriz[pos3x][pos3y] == 0 and
                   matriz[pos4x][pos4y] == 0 and matriz[pos5x][pos5y] == 0):
                    matriz[pos1x][pos1y] = 1
                    matriz[pos2x][pos2y] = 1
                    matriz[pos3x][pos3y] = 1
                    matriz[pos4x][pos4y] = 1
                    matriz[pos5x][pos5y] = 1
                    validP = True

            if shape_actual.get_type() == 2:
                pos1x = int((valueX-50+350)/50)
                pos1y = int((valueY+50+250)/50)

                pos2x = int((valueX+350)/50)
                pos2y = int((valueY+50+250)/50)

                pos3x = int((valueX+50+350)/50)
                pos3y = int((valueY+50+250)/50)

                pos4x = int((valueX-50+350)/50)
                pos4y = int((valueY+250)/50)

                pos5x = int((valueX-50+350)/50)
                pos5y = int((valueY-50+250)/50)
                if(matriz[pos1x][pos1y] == 0 and matriz[pos2x][pos2y] == 0 and matriz[pos3x][pos3y] == 0 and
                   matriz[pos4x][pos4y] == 0 and matriz[pos5x][pos5y] == 0):
                    matriz[pos1x][pos1y] = 1
                    matriz[pos2x][pos2y] = 1
                    matriz[pos3x][pos3y] = 1
                    matriz[pos4x][pos4y] = 1
                    matriz[pos5x][pos5y] = 1
                    validP = True

            if shape_actual.get_type() == 3:
                pos1x = int((valueX+350)/50)
                pos1y = int((valueY+50+250)/50)

                pos2x = int((valueX+50+350)/50)
                pos2y = int((valueY+50+250)/50)

                pos3x = int((valueX+50+350)/50)
                pos3y = int((valueY+250)/50)

                pos4x = int((valueX+50+350)/50)
                pos4y = int((valueY-50+250)/50)
                if(matriz[pos1x][pos1y] == 0 and matriz[pos2x][pos2y] == 0 and matriz[pos3x][pos3y] == 0 and
                   matriz[pos4x][pos4y] == 0):
                    matriz[pos1x][pos1y] = 1
                    matriz[pos2x][pos2y] = 1
                    matriz[pos3x][pos3y] = 1
                    matriz[pos4x][pos4y] = 1
                    validP = True

            if shape_actual.get_type() == 4:
                pos1x = int((valueX+50+350)/50)
                pos1y = int((valueY+50+250)/50)

                pos2x = int((valueX+50+350)/50)
                pos2y = int((valueY+250)/50)

                pos3x = int((valueX+50+350)/50)
                pos3y = int((valueY-50+250)/50)

                pos4x = int((valueX+350)/50)
                pos4y = int((valueY-50+250)/50)
                if(matriz[pos1x][pos1y] == 0 and matriz[pos2x][pos2y] == 0 and matriz[pos3x][pos3y] == 0 and
                   matriz[pos4x][pos4y] == 0):
                    matriz[pos1x][pos1y] = 1
                    matriz[pos2x][pos2y] = 1
                    matriz[pos3x][pos3y] = 1
                    matriz[pos4x][pos4y] = 1
                    validP = True
            if shape_actual.get_type() == 5:
                pos1x = int((valueX+350)/50)
                pos1y = int((valueY+250)/50)

                pos2x = int((valueX-50+350)/50)
                pos2y = int((valueY+250)/50)

                pos3x = int((valueX-50+350)/50)
                pos3y = int((valueY-50+250)/50)

                pos4x = int((valueX+350)/50)
                pos4y = int((valueY-50+250)/50)
                if(matriz[pos1x][pos1y] == 0 and matriz[pos2x][pos2y] == 0 and matriz[pos3x][pos3y] == 0 and
                   matriz[pos4x][pos4y] == 0):
                    matriz[pos1x][pos1y] = 1
                    matriz[pos2x][pos2y] = 1
                    matriz[pos3x][pos3y] = 1
                    matriz[pos4x][pos4y] = 1
                    validP = True
            if shape_actual.get_type() == 6:
                pos1x = int((valueX+350)/50)
                pos1y = int((valueY+250)/50)

                if(matriz[pos1x][pos1y] == 0):
                    matriz[pos1x][pos1y] = 1
                    validP = True
            if shape_actual.get_type() == 7:
                pos1x = int((valueX-50+350)/50)
                pos1y = int((valueY+250)/50)

                pos2x = int((valueX+350)/50)
                pos2y = int((valueY+250)/50)

                pos3x = int((valueX+50+350)/50)
                pos3y = int((valueY+250)/50)
                if(matriz[pos1x][pos1y] == 0 and matriz[pos2x][pos2y] == 0 and matriz[pos3x][pos3y] == 0):
                    matriz[pos1x][pos1y] = 1
                    matriz[pos2x][pos2y] = 1
                    matriz[pos3x][pos3y] = 1
                    validP = True
            if shape_actual.get_type() == 8:
                pos1x = int((valueX+350)/50)
                pos1y = int((valueY+50+250)/50)

                pos2x = int((valueX+350)/50)
                pos2y = int((valueY+250)/50)

                pos3x = int((valueX+350)/50)
                pos3y = int((valueY-50+250)/50)
                if(matriz[pos1x][pos1y] == 0 and matriz[pos2x][pos2y] == 0 and matriz[pos3x][pos3y] == 0):
                    matriz[pos1x][pos1y] = 1
                    matriz[pos2x][pos2y] = 1
                    matriz[pos3x][pos3y] = 1
                    validP = True
            if validP:
                dragging = False
                game_shapes[shape_index].set_midpoint_xy(valueX, valueY)
                game_shapes.remove(shape_actual)
                set_elegible_shapes(1)
                validate_line()
                test_actual_shapes()
                return True
    return False


def mouseControl(button, state, x, y): #Verifica que cuando el usuario da click sea para agarrar o soltar una figura
    global dragging
    global tempX
    global tempY
    global shape_index
    if not lose:
        tempX = -width / 2 + width * x / width
        tempY = height / 2 - height * y / height
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not dragging:
            check_figure(tempX, tempY)
            glutPassiveMotionFunc(passive_mouse_control)
        elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and dragging:
            if not valid_movement():
                elegible_shapes.append(game_shapes[shape_index])
                game_shapes.remove(game_shapes[shape_index])
            shape_index = None
            glutPassiveMotionFunc(None)
            dragging = False
            tempX = 0
            tempY = 0

        glutPostRedisplay()


def main():
    printInteraction()
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("Wood Blocks Game - Proyecto Intermedio")

    # Funciones de control
    glutDisplayFunc(displayMe)
    glutReshapeFunc(resize)
    glutMouseFunc(mouseControl)
    glutKeyboardFunc(keyInput)
    init()
    glutMainLoop()


main()

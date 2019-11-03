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

def generate_board():
    # print(square_module.shapes)
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

    for square in board_squares:
        square.draw_square()


def move_figure():
    pass


def drawSlider():
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_POLYGON)
    glVertex2d(200, 300)  # Superior izquierda
    glVertex2d(200, -300)  # Inferior izquierda
    glVertex2d(400, -300)  # Inferior derecha
    glVertex2d(400, 300)  # Superior derecha
    glEnd()


# OpenGL functions
def printInteraction():
    print("Wood Block Game")


def init():
    # red, green, blue, alpha from 0.0 to 1.0
    glClearColor(1.0, 1.0, 1.0, 0.0)
    


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
    if key == '+':
        tempX += 1
        glutPostRedisplay()
    if key == '-':
        tempY += 1
        glutPostRedisplay()

def set_elegible_shapes(number):
    for count in range(number):
        

def draw_shapes():
    x = 0
    y = 0

    for count in range(3):
        glColor3ub(255, 0, 0)

        shape = square_module.shapes[
            random.randint(
                0,
                len(square_module.shapes)-1)]

        shape.draw_shape(300, y)
        y += 150
    # glutPostRedisplay()


def draw_game_shapes():
    for shape in game_shapes:
        shape.draw_shape(shape.get_midpoint_x(), shape.get_midpoint_y())


def displayMe():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    drawSlider()
    generate_board()
    draw_shapes()
    draw_game_shapes()
    print("FIGURAS EN EL ARREGLO: ", len(square_module.shapes))
    glFlush()
    glutSwapBuffers()


def check_figure(x, y):
    #print("---------NUEVO FOR DE FIGURAS-------------")
    global shape_index
    shape_index = None
    for shape in square_module.shapes:
        if shape.in_range(x, y):
            game_shapes.append(shape)
            shape_index = game_shapes.index(shape)
            print(shape_index)
            global dragging
            dragging = True
            #print("Clickeaste en una figura")


def passive_mouse_control(x, y):
    # print("PASIVAAAAAAAAAAAAAAAaa")
    global tempX
    tempX = -width / 2 + width * x / width
    global tempY
    tempY = height / 2 - height * y / height
    if(dragging):
        # print("ARRASTRANDOOOO")
        game_shapes[shape_index].set_midpoint_xy(tempX, tempY)
    glutPostRedisplay()


def mouseControl(button, state, x, y):
    global dragging
    global tempX
    tempX = -width / 2 + width * x / width
    global tempY
    tempY = height / 2 - height * y / height
    #print("tempX: ", tempX, "tempY: ", tempY)
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not dragging:
        # print("CLICKEADO")
        print("tempX: ", tempX, "tempY: ", tempY)
        check_figure(tempX, tempY)
        glutPassiveMotionFunc(passive_mouse_control)
    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and dragging:
        shape_index = None
        print("Entro a donde no debe entrar, pa")
        glutPassiveMotionFunc(None)
        dragging = False
        tempX = 0
        tempY = 0
    # glutPostRedisplay()


def ciclo():
    if tempX > 0:
        glLoadIdentity()
    # glutPostRedisplay()


def main():
    printInteraction()
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("Wood Blocks")

    # Funciones de control
    glutDisplayFunc(displayMe)
    glutReshapeFunc(resize)
    glutMouseFunc(mouseControl)
    glutKeyboardFunc(keyInput)
    init()
    # glutIdleFunc(ciclo)
    glutMainLoop()


main()

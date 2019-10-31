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
shape_index = 0
init = True


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
        tempX+=1
        glutPostRedisplay()
    if key == '-':
        tempY+=1
        glutPostRedisplay()


def draw_shapes():
    x = 0
    y = 0

    for shape in square_module.shapes:
        glColor3ub(random.randint(0, 255),
                   random.randint(0, 255),
                   random.randint(0, 255))
        shape.draw_shape(shape.get_midpoint_x(), shape.get_midpoint_y())
        y += 150
    # glutPostRedisplay()


def displayMe():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    drawSlider()
    generate_board()
    draw_shapes()
    print("FIGURAS EN EL ARREGLO: ", len(square_module.shapes))
    # glFlush()
    glutSwapBuffers()


def check_figure(x, y):
    #print("---------NUEVO FOR DE FIGURAS-------------")
    for shape in square_module.shapes:
        if shape.in_range(x, y):
            shape_index = square_module.shapes.index(shape)
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
        square_module.shapes[shape_index].set_midpoint_xy(tempX, tempY)
    glutPostRedisplay()


def mouseControl(button, state, x, y):
    global tempX
    tempX = -width / 2 + width * x / width
    global tempY
    tempY = height / 2 - height * y / height
    #print("tempX: ", tempX, "tempY: ", tempY)
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # print("CLICKEADO")
        check_figure(tempX, tempY)
        glutPassiveMotionFunc(passive_mouse_control)

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

import sys
import math
#import helper
# OpenGL functions

from OpenGL.GL import *
from OpenGL.GLUT import *  # GL Utilities Toolkit
from OpenGL.GLU import *

height = 500
width = 500

t = 0.0
# Radio de los nodos
R = 80.0
PI = 3.14159265358979324
# Numero de vertices de las transiciones y los nodos
numVertices = 50
move = 0

tamano = 50

moveX = 0
moveY = 0

angulo = 0
anguloT = 0
tipo = 0
tipo2 = 0
velocidad = 0.4
bandera = False

# Lineas verticales
linea1_1 = -100
linea1_2 = -110
linea2_1 = 100
linea2_2 = 110

# Lineas Horizontales
linea3_1 = -100
linea3_2 = -110
linea4_1 = 100
linea4_2 = 110

# Lineas diagonales
linea5_x1 = 0
linea5_x2 = 0
linea5_y1 = 0
linea5_y2 = 0
linea6_x1 = 0
linea6_x2 = 0
linea6_y1 = 0
linea6_y2 = 0

# Globals.
R = (tamano / 2) + 10
# Radius of circle.
X = 00.0
# X-coordinate of center of circle.
Y = -tamano / 2
# Y-coordinate of center of circle.
numVertices = 40


def printInteraction():
    print("Author: Raul Alejandro Lopez Balleza - 1730425")
    print("Objective:")


def init():
    # red, green, blue, alpha from 0.0 to 1.0
    glClearColor(0.0, 0.0, 0.0, 0.0)
    # Informacion en pantalla


# Keep the aspect ratio of the graphics window and
# anything we draw will look in proper proportion
# OpenGL set w and h values as the graphics window's size changes
def resize(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Set viewing box dimensions equal to window dimensions.
    glOrtho(0.0, w, 0.0, h, -1.0, 1.0)

    # Pass the size of the OpenGL window to globals.
    width = w
    height = h

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def displayMe():
    glClear(GL_COLOR_BUFFER_BIT)
    drawCircle()
    drawCutLines1()
    glFlush()


def main():
    printInteraction()
    glutInit(sys.argv)
    # Si el usuario proporcina un argumento y es un archivo .csv entonces el codigo continua ejecutandose, sino, el programa se detiene
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("GIF")

    # Funciones de control
    glutDisplayFunc(displayMe)
    glutReshapeFunc(resize)
    init()
    glutMainLoop()


main()


from OpenGL.GL import *
from OpenGL.GLUT import *  # GL Utilities Toolkit
from OpenGL.GLU import *

ESCAPE = as_8_bit('\033')
font = GLUT_BITMAP_8_BY_13  # Fuente global a utilizar

data = []  # Arreglo que guardara la informacion del archivo proporcionado despues


def readCSV():
    # Lee el archivo linea por linea y la agrega al arreglo data
    with open(sys.argv[1]) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            data.append(row)


def escribirFuente(fuente, texto, x, y):
    glColor3f(0.0, 0.0, 0.0)    # Fuente en color negro
    glRasterPos3f(x, y, 0.0)    # Fijar posicion de escritura
    # Escribir caracter por caracter
    for ch in texto:
        glutBitmapCharacter(fuente, ctypes.c_int(ord(ch)))


def midPointX(x1, x2):  # Regresa el punto medio entre dos puntos X
    return (x1 + x2) / 2


def midPointY(y1, y2):  # Regresa el punto medio entre dos puntos Y
    return (y1 + y2) / 2


def distance(x1, x2, y1, y2):  # Regresa la distancia entre dos puntos (x1,y1) y (x2,y2)
    return math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))

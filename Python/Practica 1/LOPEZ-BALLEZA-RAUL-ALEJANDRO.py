# Ejecucion:
'''
DESARROLLADO POR: RAUL ALEJANDRO LOPEZ BALLEZA
Cargar el archivo .csv con datos de entrada para la correcta ejecucion del programa,
se adjunta un archivo de prueba que muestra como debe ser la estructura del archivo.
El programa generara los "nodos" de los estados y sus transisiones con los demas nodos o hacia asi mismo.
Las lineas azules representan que esa transicion es una entrada de 1.
Las lineas rojas representan que esa transicion es una entrada de 0.
Una vez generados los "nodos" y las transiciones se mostrará el diagrama de maquina de estado

EJEMPLO DE ESTRUCTURA DE ARCHIVO:
"ESTADO INICIAL", "ENTRADA", "ESTADO FINAL"
    000             1           001
    001             0           000
    000             1           000
El archivo debera contener al menos 3 entradas por linea, estado inicial, entrada y estado final.
tomando valores binarios en cualquiera de las 3.
Estos deberan estar separados por comas, sin espacios y cada "transicion" debera ser en una nueva linea
'''
# python3 stateMachine.py
# Libreria math para funciones de cos y sin
import math
# Libreria csv para leer el archivo de datos
import csv
# Librerias de openGL
from OpenGL.GL import *
from OpenGL.GLUT import *  # GL Utilities Toolkit
from OpenGL.GLU import *

# Arreglo que guardara los "nodos" creados
Nodes = []
# Arreglo que guardara la informacion del archivo proporcionado despues
data = []
# Arreglo que guardara las "Transiciones" de un nodo a otro
Relations = []

# Valores iniciales de la ventana
height = 500
width = 500
t = 0.0
# Radio de los nodos
R = 30.0
PI = 3.14159265358979324
# Numero de vertices de las transiciones y los nodos
numVertices = 50
ESCAPE = as_8_bit('\033')
# Fuente global a utilizar
font = GLUT_BITMAP_8_BY_13


# Funciones auxiliares
def escribirFuente(fuente, texto, x, y):
    # Fuente en color negro
    glColor3f(0.0, 0.0, 0.0)
    # Fijar posicion de escritura
    glRasterPos3f(x, y, 0.0)
    # Escribir caracter por caracter
    for ch in texto:
        glutBitmapCharacter(fuente, ctypes.c_int(ord(ch)))


# Recibe un elemento nodo que comparara su estado con todos lo que ya estan guardados
# para ver si es un nodo ya registrado
def isDuplicated(node):
    found = False
    for nodex in Nodes:
        if nodex.state == node.state:
            found = True
    return found


# Regresa el punto medio entre dos puntos X
def midPointX(x1, x2):
    return (x1 + x2) / 2


# Regresa el punto medio entre dos puntos Y
def midPointY(y1, y2):
    return (y1 + y2) / 2


# Regresa la distancia entre dos puntos (x1,y1) y (x2,y2)
def distance(x1, x2, y1, y2):
    return math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))


# Funciones de dibujado

# Para cada nodo en el arreglo Nodes se manda a llamar la funcion .drawNode()
def drawNodes():
    iterator = Nodes.__iter__()
    for node in iterator:
        node.drawNode()


# Para cada relacion en el arreglo Relations se manda a llamar la funcion .drawRelation(
def drawRelations():
    iterator = Relations.__iter__()
    for relation in iterator:
        relation.drawRelation()


# Funciones de creacion

def createNodes():
    x = 0
    y = 0
    for row in data:
        state = []
        r = int((len(row) - 1) / 2)
        for i in range(r):
            state.append(row[i])
        # Lee el arreglo de datos linea por linea y lo va parseando para poder crear los nodos a partis de ellos
        node = Node(state)
        # Si el nodo no ah sido "registrado" anteriormente se agrega al arreglo de nodos, que son los que se van a dibujar
        if not isDuplicated(node):
            x = x + 50
            if x > width:
                x = x - 50
            y = y + 50
            if y > height:
                y = y - 50
            Nodes.append(node)
            node.setX(x)
            node.setY(height - y)


def createRelations():
    # Lee el arreglo de datos y lo va parseando crear la relacion entre cada nodo
    for d in data:
        r = int((len(d) - 1) / 2)
        state = []
        state2 = []
        for i in range(r):
            state.append(d[i])
        input = d[r]
        r = r + 1
        for k in range(r, len(d)):
            state2.append(d[k])
        for initNode in Nodes:
            if initNode.state == state:
                for destNode in Nodes:
                    if destNode.state == state2:
                        # Si la informacion de los nodos coincide con la linea consultada se crea una relacion entre esos
                        # nodos y se agrega al arreglo de relaciones
                        relation = Relation(initNode, destNode, input)
                        Relations.append(relation)
    # print(Relations)


# Object classes
class Node:
    def __init__(self, state):
        self.state = state

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def drawNode(self):
        t = 0
        text = ''
        glPolygonMode(GL_FRONT, GL_FILL)
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_POLYGON)
        for i in range(numVertices):
            glVertex2d(self.x + R * math.cos(t), self.y + R * math.sin(t))
            t += 2 * PI / numVertices
        glEnd()
        '''glBegin(GL_LINE_LOOP)
        for i in range(numVertices):
            #glColor3ub(0, 0, 0)
            glVertex3f(self.x + R * math.cos(t), self.y + R * math.sin(t), 0.0)
            t += 2 * PI / numVertices
        glEnd()'''
        for f in self.state:
            text += f
        escribirFuente(font, str(text), self.x - R / 4, self.y)


class Relation:
    def __init__(self, initNode, destNode, input):
        self.initNode = initNode
        self.destNode = destNode
        self.input = input
        # Si el nodo inicial es el mismo que el nodo final entonces se dibuja un retorno hacia el mismo
        if initNode.state == destNode.state:
            if input == '0':
                self.x1 = initNode.x - R
                self.y1 = initNode.y - (R * 2)
                self.x2 = destNode.x - (R * 2)
                self.y2 = destNode.y - R
            else:
                self.x1 = initNode.x + R
                self.y1 = initNode.y + (R * 2)
                self.x2 = destNode.x + (R * 2)
                self.y2 = destNode.y + R

            self.Points = ((initNode.x, initNode.y, 0.0),
                           (self.x1, self.y1, 0.0), (self.x2, self.y2, 0.0),
                           (destNode.x, destNode.y, 0.0))
        else:
            # Sino, se dibuja una relacion entre dos nodos diferentes
            self.x = midPointX(initNode.x, destNode.x)
            self.y = midPointY(initNode.y, destNode.y)
            self.radio = distance(initNode.x, destNode.x, initNode.y, destNode.y) / 2
            if input == '0':
                self.Points = ((initNode.x, initNode.y, 0.0),
                               (self.x - self.radio, self.y - self.radio, 0.0),
                               (destNode.x, destNode.y, 0.0))
            else:
                self.Points = ((initNode.x, initNode.y, 0.0),
                               (self.x + self.radio, self.y + self.radio, 0.0),
                               (destNode.x, destNode.y, 0.0))
            # print(initNode.x, initNode.y, self.x, self.y, destNode.x, destNode.y)

    def drawRelation(self):
        glMap1f(GL_MAP1_VERTEX_3, 0.0, 1.0, self.Points)
        glEnable(GL_MAP1_VERTEX_3)
        glMapGrid1f(numVertices, 0.0, 1.0)
        # glClear(GL_COLOR_BUFFER_BIT)
        # Si la entrada es 0 entonces se dibujara una relacion roja
        text = self.input
        if self.input == '0':
            escribirFuente(font, str(text), self.x - self.radio / 2, self.y - self.radio / 2)
            glColor3f(1, 0, 0)
        else:
            # Si es 1 se dibujara una linea azul
            escribirFuente(font, str(text), self.x + self.radio / 2, self.y + self.radio / 2)
            glColor3f(0, 0, 1)

        glBegin(GL_LINE_STRIP)
        for i in range(numVertices):
            glEvalCoord1f(float(i) / numVertices)
        glEnd()
        """glPointSize(5)
        glColor3f(1, 1, 0)
        glBegin(GL_POINTS)
        for point in self.Points:
            glVertex3fv(point)
        glEnd()"""
        glFlush()


# OpenGL functions
def printInteraction():
    print("Author: Raul Alejandro Lopez Balleza - 1730425")
    print("Objective:")
    print("State machine diagram generator. It generates a SMD with the data given in the .csv file")
    print("Interaction:")
    print("Load the .csv file as first arg")
    print("Must have at least 1 initial state, 1 entry and 1 final state")
    print("Initial state and Final state could be the same")
    print("Press [ESCAPE] to finish.")
    print("Example of .csv file structure(No headers needed and comma separated values):")
    print("'Initial state'\t'Entry'\t'Final state'")
    print("000,\t\t1,\t\t101")
    print("101,\t\t0,\t\t000")
    print("Blue relations goes UP.")
    print("Red relations goes DOWN")


def init():
    # red, green, blue, alpha from 0.0 to 1.0
    glClearColor(1.0, 1.0, 0.0, 0.0)
    # Informacion en pantalla
    readCSV()


# Funcion para leer el archivo de datos proporsionado
def readCSV():
    # Lee el archivo linea por linea y la agrega al arreglo data
    with open(sys.argv[1]) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            data.append(row)


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


def keyInput(key, x, y):
    # Si la tecla presionada es el ESCAPE entonces el programa finaliza
    if key == ESCAPE:
        sys.exit()


def displayMe():
    glClear(GL_COLOR_BUFFER_BIT)
    createNodes()
    createRelations()
    drawRelations()
    drawNodes()
    # glutPostRedisplay()
    glFlush()


def mouseControl(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        text = 5
        escribirFuente(font, str(text), x, y)
    glutPostRedisplay()


def main():
    printInteraction()
    glutInit(sys.argv)
    # Si el usuario proporcina un argumento y es un archivo .csv entonces el codigo continua ejecutandose, sino, el programa se detiene
    if sys.argv[1] and sys.argv[1].endswith(".csv"):
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
        glutInitWindowSize(800, 600)
        glutInitWindowPosition(100, 100)
        glutCreateWindow("stateMachine")

        # Funciones de control
        glutDisplayFunc(displayMe)
        glutReshapeFunc(resize)
        glutMouseFunc(mouseControl)
        glutKeyboardFunc(keyInput)
        init()
        glutMainLoop()
    else:
        print("No se ah encontrado el archivo de datos, "
              "por favor ingrese el nombre del archivo "
              "como argumento al momento de ejecutar el script")
        sys.exit()


main()

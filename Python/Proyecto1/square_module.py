from OpenGL.GL import *
from OpenGL.GLUT import *  # GL Utilities Toolkit
from OpenGL.GLU import *
import random
import math

point_size = 50


def check_distance(x1, y1, x2, y2): #Checa la distancia entre dos puntos
    return math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))


class Square: #Clase para generar cada de cuadro de las figuras
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.state = 0

    def draw_square(self): #Dibuja el cuadro
        glPointSize(point_size)
        glBegin(GL_POINTS)
        glVertex2f(self.x, self.y)
        glEnd()


class Shape: #Clase de figura, cada 1 en la lista de puntos dada es un cuadro a dibujar
    def __init__(self, points_list):
        self.points = list(points_list)
        self.squares = list()
        self.midpoint_x = 0
        self.midpoint_y = 0
        self.t_figure = None

    def get_points(self): #Obtiene la lista de puntos
        return self.points

    def in_range(self, x, y):
        '''print("-----------------------------")
        print("SELF.X", self.midpoint_x, ", SELF.Y",
              self.midpoint_y, "\n X:", x, ",Y:", y)'''
        #print(check_distance(self.midpoint_x, self.midpoint_y, x, y))
        if check_distance(self.midpoint_x, self.midpoint_y, x, y) <= point_size*2:
            return True
    
    def get_midpoint_x(self): #Regresa su coordenada en X
        return self.midpoint_x

    def get_midpoint_y(self): #Regresa su coordenada en Y
        return self.midpoint_y

    def set_midpoint_xy(self, x, y): #Establece sus coordenadas x,y en los valores dados
        self.midpoint_x = x
        self.midpoint_y = y

    def set_type(self, typef):
        self.t_figure = typef

    def get_type(self):
        return self.t_figure

    def draw_shape(self, x, y): #Dibuja cada cuadro de la figura dada la lista de puntos
        self.squares.clear()
        temp_y = 0
        self.set_midpoint_xy(x, y)
        for count in range(3):
            if count == 0:
                temp_y = y + point_size
            if count == 1:
                temp_y = y
            if count == 2:
                temp_y = y - point_size

            if not self.points[0][count] == 0:
                sq = Square(x-point_size, temp_y, 1)
                self.squares.append(sq)
            if not self.points[1][count] == 0:
                sq = Square(x, temp_y, 1)
                self.squares.append(sq)
            if not self.points[2][count] == 0:
                sq = Square(x+point_size, temp_y, 1)
                self.squares.append(sq)

        for square in self.squares:
            square.draw_square()

#Establecemos los puntos par cada figua en un area de 3x3 que nos servira para darle forma a la misma
# Game shapes
shape_l = Shape(([1, 0, 0], [1, 0, 0], [1, 1, 1]))
shape_l.set_type(1)

shape_l_inverted = Shape(([1, 1, 1], [1, 0, 0], [1, 0, 0]))
shape_l_inverted.set_type(2)

shape_l_inverted_left = Shape(([0, 0, 0], [1, 0, 0], [1, 1, 1]))
shape_l_inverted_left.set_type(3)

shape_l_inverted_right = Shape(([0, 0, 0], [0, 0, 1], [1, 1, 1]))
shape_l_inverted_right.set_type(4)

shape_square = Shape(([0, 1, 1], [0, 1, 1], [0, 0, 0]))
shape_square.set_type(5)

shape_dot = Shape(([0, 0, 0], [0, 1, 0], [0, 0, 0]))
shape_dot.set_type(6)

shape_i = Shape(([0, 1, 0], [0, 1, 0], [0, 1, 0]))
shape_i.set_type(7)

shape_i_horizontal = Shape(([0, 0, 0], [1, 1, 1], [0, 0, 0]))
shape_i_horizontal.set_type(8)

#En este arreglo contendremos nuestras figuras, lo podemos ver como un "Catalogo" ya que estas nunca seran modificadas
# Shapes array
shapes = list()
shapes.append(shape_l)
shapes.append(shape_l_inverted)
shapes.append(shape_l_inverted_left)
shapes.append(shape_l_inverted_right)
shapes.append(shape_square)
shapes.append(shape_dot)
shapes.append(shape_i)
shapes.append(shape_i_horizontal)

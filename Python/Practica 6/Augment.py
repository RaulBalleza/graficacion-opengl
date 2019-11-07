#import cv2
import numpy as np
import glob
import time
import pygame

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import os.path
import getopt
NombreModelo = "usb_protector.obj"

global obj
obj = None
width = None
height = None
lightZeroPosition = [0.0, 0.0, 20.0, 1.0]
lightZeroColor = [2.5, 2.5, 2.5, 1]
AnguloX = 0


def MTL(filename):
    contents = {}
    mtl = None
    for line in open(filename, "r"):
        if line.startswith('#'):
            continue
        values = line.split()
        if not values:
            continue
        if values[0] == 'newmtl':
            mtl = contents[values[1]] = {}
        elif mtl is None:
            raise ValueError("mtl file doesn't start with newmtl stmt")
            # X=1
        elif values[0] == 'map_Kd':
            # load the texture referred to by this declaration
            #mtl[values[0]] = values[1]
            #mtl[values[0]] = map(float, values[1:])
            print("Valor de values", len(values), values[1], values[1:])
            if len(values) == 2:
                ValerVerg = 1
                surf = pygame.image.load(values[1])
                image = pygame.image.tostring(surf, 'RGBA', 1)
                ix, iy = surf.get_rect().size
                texid = glGenTextures(1)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                                GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                                GL_LINEAR)
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA,
                             GL_UNSIGNED_BYTE, image)

            else:
                mtl[values[0]] = list(map(float, values[1:]))

        elif values[0] == 'map_Ka':
            # load the texture referred to by this declaration
            #mtl[values[0]] = values[1]
            #mtl[values[0]] = map(float, values[1:])
         #           print ("Valor de values",values[1],values[1:])
            print("Valor de values", values[0], len(
                values), values[1], values[1:])
            if len(values) == 2:  # Incluye una Textura!
                ValerVerg = 1
                surf = pygame.image.load(values[1])
                image = pygame.image.tostring(surf, 'RGBA', 1)
                ix, iy = surf.get_rect().size
                texid = glGenTextures(1)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                                GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                                GL_LINEAR)
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA,
                             GL_UNSIGNED_BYTE, image)

            else:
                mtl[values[0]] = list(map(float, values[1:]))

        else:
            #mtl[values[0]] = map(float, values[1:])
            mtl[values[0]] = list(map(float, values[1:]))
    return contents


class OBJ:
    def __init__(self, filename, swapyz=False):
        """Loads a Wavefront OBJ file. """
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []

        material = None
        for line in open(filename, "r"):
            if line.startswith('#'):
                continue
            values = line.split()
            if not values:
                continue
            if values[0] == 'v':
                #v = map(float, values[1:4])
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
            elif values[0] == 'vn':
                #                v = map(float, values[1:4])
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.normals.append(v)
            elif values[0] == 'vt':
                #self.texcoords.append(map(float, values[1:3]))
                self.texcoords.append(list(map(float, values[1:3])))
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'mtllib':
                self.mtl = MTL(values[1])
            elif values[0] == 'f':
                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self.faces.append((face, norms, texcoords, material))

        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)
        for face in self.faces:
            vertices, normals, texture_coords, material = face

            mtl = self.mtl[material]
            if 'texture_Kd' in mtl:
                # use diffuse texmap
                glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
            else:
                # just use diffuse colour
                glColor(*mtl['Kd'])

            glBegin(GL_POLYGON)
            for i in range(len(vertices)):
                if normals[i] > 0:
                    glNormal3fv(self.normals[normals[i] - 1])
                if texture_coords[i] > 0:
                    glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
                glVertex3fv(self.vertices[vertices[i] - 1])
            glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()


def keyboard(key, x, y):
    if key.decode("utf-8") == 'q':
        global cap
        cap.release()
        cv2.destroyAllWindows()
        exit()
    if key.decode("utf-8") == ' ':
        global spheres
        spheres = not spheres


def display():
    global fovy, aspectRatio, dist_co, cameraMatrix, currFrame, output, spheres
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glViewport(0, 0, width, height)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-1.0, 1.0, -1.0, 1.0, 1, 500)
    glMatrixMode(GL_MODELVIEW)

    glLoadIdentity()

    glColor3f(1.0, 1.0, 1.0)
    glLoadIdentity()
    # glRotatef(180,0.0,1.0,0.0);
    # glTranslatef(0.0,0.0,50.0);

    glTranslatef(0.0, 0.0, -10.0)
    glRotatef(AnguloX, 0.0, 1.0, 0.0)

    glCallList(obj.gl_list)

    glLoadIdentity()
    glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)

    glutSwapBuffers()
    glutPostRedisplay()

#
# OpenGl reshape
#


def reshape(w, h):
    glViewport(0, 0, w, h)
#
# OpenGL Idle Loop
#


def idle():
    global AnguloX
    AnguloX = AnguloX+1

#    currFrame=cv2.imread("QRsNuevos.png")
    #ret, frame = cap.read()
    # if ret is True:
    #   currFrame = frame
#
# Main Camera Calibration and OpenGL loop
#


def main():
    global width, height

    # loadParams('web_camera_params.txt')
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

    width = 500
    height = 500

    glutInitWindowSize(width, height)
    glutCreateWindow("OpenGL / OpenCV Example")

#    glEnable(GL_LIGHTING)
 #   glEnable(GL_LIGHT0)
  #  glEnable(GL_COLOR_MATERIAL)
   #	 glEnable(GL_CULL_FACE)

    # we cull the front faces because my depth values are reversed from typical 0 to 1
    glCullFace(GL_FRONT)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_DEPTH_TEST)

    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutReshapeFunc(reshape)
    glutIdleFunc(idle)

    #glLightfv(GL_LIGHT0, GL_POSITION,  (0, 0, 5, 0.0))

    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    # most obj files expect to be smooth-shaded
    glShadeModel(GL_SMOOTH)

    global obj
    obj = OBJ(NombreModelo, swapyz=True)

    glutMainLoop()


if __name__ == '__main__':
    main()

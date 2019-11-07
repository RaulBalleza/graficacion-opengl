/* File for "Putting It All Together" lesson of the OpenGL tutorial on
 www.videotutorialsrock.com
Modificado por: Marco Aurelio Nuño Maganda
Adaptado para la Clase "Introducción a la Graficación por Computadora"
Universidad Politécnica de Victoria
Última Modificación: 11 de Octubre de 2012
 */

#include <iostream>
#include <stdlib.h>

#ifdef __APPLE__
#include <OpenGL/OpenGL.h>
#include <GLUT/glut.h>
#else
#include <GL/glut.h>
#endif

//#include "imageloader.h"

using namespace std;

GLfloat headVerticalAngle = 0.0;
GLfloat headHorizontalAngle = 0.0;
GLfloat legsAngle = 0.0;
GLfloat tailVerticalAngle = 0.0;
GLfloat tailHorizontalAngle = 0.0;
GLfloat tailWiggleAngle = 0.0;

const float BOX_SIZE = 4.0f; //The length of each side of the cube
float Angulo = 0;            //The rotation of the box
GLuint _textureId;           //The OpenGL id of the texture

void handleKeypress(unsigned char key, int x, int y)
{
    switch (key)
    {
    case 27: //Escape key
        exit(0);
        break;
    case ' ':
        legsAngle += 0.1;
        cout << "Legs Angle:" << legsAngle;
        glutPostRedisplay();
        break;
    }
}

void initRendering()
{
    glEnable(GL_DEPTH_TEST);
}

void handleResize(int w, int h)
{
    glViewport(0, 0, w, h);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(45.0, (float)w / (float)h, 1.0, 200.0);
}

void drawScene()
{
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    glTranslatef(0.0f, 0.0f, -5.0f);
    glRotatef(-Angulo, 1.0f, 1.0f, 0.0f);

    glPushMatrix();
    GLfloat color[4] = {0.92f, 0.814f, 0.382f, 1.0f};
    glColor4fv(color);

    GLfloat dog_specular[] = {0.1f, 0.1f, 0.1f},
            dog_shininess = 0.1f;

    glMaterialfv(GL_FRONT, GL_SPECULAR, dog_specular);
    glMaterialf(GL_FRONT, GL_SHININESS, dog_shininess);
    glMaterialf(GL_FRONT, GL_EMISSION, 0);
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, color);

    //torso
    glPushMatrix();
    glScalef(2.0f * 0.3f, 2.0f * 0.3f, 4.0f * 0.3f);
    glutSolidSphere(1, 30, 30);
    glPopMatrix();

    //legs
    glPushMatrix();
    glRotatef(legsAngle, 1, 0, 0);
    glTranslated(-1 * 0.3, -2.5 * 0.3, -2 * 0.3);
    glScalef(0.5f * 0.3f, 2.0f * 0.3f, 0.5f * 0.3f);
    glutSolidSphere(1, 30, 30);
    glPopMatrix();

    glPushMatrix();
    glRotatef(-legsAngle, 1, 0, 0);
    glTranslated(0.3f, -2.5f * 0.3f, -0.6);
    glScalef(0.5f * 0.3f, 0.6f, 0.5f * 0.3f);
    glutSolidSphere(1, 30, 30);
    glPopMatrix();

    glPushMatrix();
    glRotatef(legsAngle, 1, 0, 0);
    glTranslated(0.3f, -2.5f * 0.3f, 2.0 * 0.3f);
    glScalef(0.5f * 0.3f, 2.0f * 0.3f, 0.5f * 0.3f);
    glutSolidSphere(1, 30, 30);
    glPopMatrix();

    glPushMatrix();
    glRotatef(-legsAngle, 1, 0, 0);
    glTranslated(-0.3f, -2.5f * 0.3f, 0.6);
    glScalef(0.5f * 0.3f, 2.0f * 0.3f, 0.5f * 0.3f);
    glutSolidSphere(1, 30, 30);
    glPopMatrix();

    //tail
    glPushMatrix();
    glTranslated(0.0f, 0.0f, -3.8f * 0.3f);
    glRotatef(-30, 1, 0, 0);
    glRotatef(tailVerticalAngle, 1, 0, 0);
    glRotatef(tailHorizontalAngle, 0, 1, 0);
    glRotatef(tailWiggleAngle, 0, 1, 0);
    glScalef(0.5f * 0.3f, 0.5f * 0.3f, 1.8f * 0.3f);

    glutSolidSphere(1, 30, 30);
    glPopMatrix();

    //head rotation
    glPushMatrix();
    glRotatef(headVerticalAngle, 1, 0, 0);
    glRotatef(headHorizontalAngle, 0, 1, 0);

    //head
    glPushMatrix();
    glTranslated(0.0f, 2.5f * 0.3f, 3.0f * 0.3f);
    glScalef(1.5f * 0.3f, 1.55f * 0.3f, 1.6f * 0.3f);
    glutSolidSphere(1, 30, 30);
    glPopMatrix();

    //nose
    glPushMatrix();
    glTranslated(0.0f, 2.2f * 0.3f, 4.2f * 0.3f);
    glScalef(0.8f * 0.3f, 0.5f * 0.3f, 1.5f * 0.3f);
    glutSolidSphere(1, 30, 30);
    glPopMatrix();

    //ears
    glPushMatrix();
    glTranslated(-0.8f * 0.3f, 3.8f * 0.3f, 2.6f * 0.3f);
    glScalef(0.5f * 0.3f, 0.3f, 0.5f * 0.3f);
    glutSolidSphere(1, 30, 30);
    glPopMatrix();

    glPushMatrix();
    glTranslated(0.8f * 0.3f, 3.8f * 0.3f, 2.6f * 0.3f);
    glScalef(0.5f * 0.3f, 1.0f * 0.3f, 0.5f * 0.3f);
    glutSolidSphere(1, 30, 30);
    glPopMatrix();

    //eyes
    GLfloat eyes_specular[] = {0.4f, 0.4f, 0.4f},
            eyes_shininess = 1.0f;
    GLfloat black[] = {0, 0, 0, 1};
    glColor4fv(black);
    glMaterialfv(GL_FRONT, GL_SPECULAR, eyes_specular);
    glMaterialf(GL_FRONT, GL_SHININESS, eyes_shininess);
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, black);

    glPushMatrix();
    glTranslated(0.5f * 0.3f, 3.0f * 0.3f, 4.4f * 0.3f);
    glScalef(0.25f * 0.3f, 0.25f * 0.3f, 0.25f * 0.3f);
    glutSolidCube(1);
    glPopMatrix();

    glPushMatrix();
    glTranslated(-0.5f * 0.3f, 3.0f * 0.3f, 4.4f * 0.3f);
    glScalef(0.25f * 0.3f, 0.25f * 0.3f, 0.25f * 0.3f);
    glutSolidCube(1);
    glPopMatrix();

    glPopMatrix();

    glPopMatrix();

    glutSwapBuffers();
}

//Called every 25 milliseconds
void update(int value)
{
    Angulo += 1.0f;
    if (Angulo > 360)
    {
        Angulo -= 360;
    }
    glutPostRedisplay();
    glutTimerFunc(25, update, 0);
}

int main(int argc, char **argv)
{
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
    glutInitWindowSize(400, 400);

    glutCreateWindow("CUBO !!!");
    initRendering();

    glutDisplayFunc(drawScene);
    glutKeyboardFunc(handleKeypress);
    glutReshapeFunc(handleResize);
    glutTimerFunc(25, update, 0);

    glutMainLoop();
    return 0;
}

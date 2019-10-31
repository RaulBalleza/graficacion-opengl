/*DESARROLLADO POR RAUL ALEJADNDRO LOPEZ BALLEZA*/
#include "Dog.cpp"
#include <iostream>
#include <GL/glew.h>
#include <GL/freeglut.h>
// Use the STL extension of C++.
using namespace std;

// Globals.
static int width, height; // OpenGL wi  ndow size.
int tempX, tempY;
char *texto = new char();

void drawScene(void) //Funcion de dibujado principal
{
    Dog dog = Dog();
    dog.draw();
}

// OpenGL window reshape routine.
void resize(int w, int h)
{
    glViewport(0, 0, w, h);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();

    // Set viewing box dimensions equal to window dimensions.
    glOrtho(-w / 2, w / 2, -h / 2, h / 2, -1.0, 1.0);

    // Pass the size of the OpenGL window to globals.
    width = w;
    height = h;

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
}

// Keyboard input processing routine.
void keyInput(unsigned char key, int x, int y)
{
    switch (key)
    {
    case 27:
        exit(0);
        break;
    default:
        break;
    }
}

// Initialization routine.
void setup(void)
{
    glClearColor(1.0, 1.0, 1.0, 0.0);
}
// Routine to output interaction instructions to the C++ window.
void printInteraction(void)
{
    cout << "/*DESARROLLADO POR RAUL ALEJADNDRO LOPEZ BALLEZA*/" << endl;
    cout << "Interaccion:" << endl;
}

// Main routine.
int main(int argc, char **argv)
{
    printInteraction();
    glutInit(&argc, argv);
    glutInitContextVersion(4, 3);
    glutInitContextProfile(GLUT_COMPATIBILITY_PROFILE);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA);
    glutInitWindowSize(600, 600);
    glutInitWindowPosition(100, 100);
    glutCreateWindow("Perro 3D en OpenGL");
    glutDisplayFunc(drawScene);

    glutReshapeFunc(resize);
    glutKeyboardFunc(keyInput);
    glewExperimental = GL_TRUE;
    glewInit();
    setup();
    glutMainLoop();
}
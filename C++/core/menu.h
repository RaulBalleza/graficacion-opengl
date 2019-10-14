#include "librerias.h"

//Variables de opciones
static int isGrid = 1;
static int isAxis = 1;
static int isRule = 1;
static int isSub = 1;
static int isSum = 1;
static int isP = 1;
void rightMenu(int id)
{
    if (id == 1)
        exit(0);
}

void grid_menu(int id)
{
    if (id == 3)
        isGrid = 1;
    if (id == 4)
        isGrid = 0;
    glutPostRedisplay();
}

void axis_menu(int id)
{
    if (id == 5)
        isAxis = 1;
    if (id == 6)
        isAxis = 0;
    glutPostRedisplay();
}

void P_menu(int id)
{
    if (id == 7)
        isP = 1;
    if (id == 8)
        isP = 0;
    glutPostRedisplay();
}

void Sum_menu(int id)
{
    if (id == 9)
        isSum = 1;
    if (id == 10)
        isSum = 0;
    glutPostRedisplay();
}

void Sub_menu(int id)
{
    if (id == 11)
        isSub = 1;
    if (id == 12)
        isSub = 0;
    glutPostRedisplay();
}

void Paralelogram_menu(int id)
{
    if (id == 12)
        isRule = 1;
    if (id == 14)
        isRule = 0;
    glutPostRedisplay();
}
void makeMenu(void)
{
    int sub_menu;
    sub_menu = glutCreateMenu(grid_menu);
    glutAddMenuEntry("On", 3);
    glutAddMenuEntry("Off", 4);

    int sub_menu2;
    sub_menu2 = glutCreateMenu(axis_menu);
    glutAddMenuEntry("On", 5);
    glutAddMenuEntry("Off", 6);

    int sub_menu3;
    sub_menu3 = glutCreateMenu(P_menu);
    glutAddMenuEntry("On", 7);
    glutAddMenuEntry("Off", 8);

    int sub_menu4;
    sub_menu4 = glutCreateMenu(Sum_menu);
    glutAddMenuEntry("On", 9);
    glutAddMenuEntry("Off", 10);

    int sub_menu5;
    sub_menu5 = glutCreateMenu(Sub_menu);
    glutAddMenuEntry("On", 11);
    glutAddMenuEntry("Off", 12);

    int sub_menu6;
    sub_menu6 = glutCreateMenu(Paralelogram_menu);
    glutAddMenuEntry("On", 13);
    glutAddMenuEntry("Off", 14);

    glutCreateMenu(rightMenu);
    glutAddSubMenu("Grid", sub_menu);
    glutAddSubMenu("Axis", sub_menu2);
    glutAddSubMenu("P", sub_menu3);
    glutAddSubMenu("Sum", sub_menu4);
    glutAddSubMenu("Sub", sub_menu5);
    glutAddSubMenu("Paralelogram", sub_menu6);

    glutAddMenuEntry("Quit", 1);
    glutAttachMenu(GLUT_RIGHT_BUTTON);
}
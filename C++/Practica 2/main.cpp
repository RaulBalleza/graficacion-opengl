#include "../core/text.h"
#include "../core/point.h"
#include "../core/slider.h"
#include "../core/menu.h"
// Use the STL extension of C++.
using namespace std;

// Globals.
static int width, height; // OpenGL window size.
int tempX, tempY;
//Variables de dibujado sincronizado
float aumentarXS1 = 0;
float aumentarYS1 = 0;
float aumentarXS2 = 0;
float aumentarYS2 = 0;
static float pixel = 30;                      //Tamaño de cada cuadro del mapa
static long font = (long)GLUT_BITMAP_8_BY_13; // Font selection.
float s1_[2] = {0, 0};
float s2_[2] = {0, 0};
Point *CP = NULL;
Point P = Point(-pixel, 4 * pixel);
Point O = Point(0, 0);
vector<Point> ParalelGr{Point(0, 0), Point(0, 0), Point(0, 0), Point(0, 0)};
static Slider s1 = Slider(8 * pixel, 9 * pixel, 10);
static Slider s2 = Slider(8 * pixel, 8 * pixel, 10);
char *texto = new char();

//FUNCIONES AUXILIARES

float distanceX(Point p0, Point p1) //Mide la distancia en X entre 2 punto
{
    return abs(sqrt(pow(p0.getX() - p1.getX(), 2)));
}

float distanceY(Point p0, Point p1) //Mide la distancia en Y entre 2 puntos
{
    return abs(sqrt(pow(p0.getY() - p1.getY(), 2)));
}

bool inRange(unsigned low, unsigned high, unsigned x) /*Detecta si se ah dado click en 
algun punto dibujado en el mapa*/
{
    return ((x - low) <= (high - low));
}

void drawP() //Dibuja el punto P
{
    glColor3f(0.0, 0.0, 0.0);
    glBegin(GL_LINES);
    glVertex2i(O.getX(), O.getY());
    glVertex2i(P.getX(), P.getY());
    glEnd();
    P.drawPoint();
}

void drawParalelogramo() //Dibuja el area del paralelogramo
{
    ParalelGr.at(0).setX(O.getX());
    ParalelGr.at(0).setY(O.getY());

    ParalelGr.at(1).setX(ParalelGr.at(0).getX() + s1_[0] * aumentarXS1);
    ParalelGr.at(1).setY(ParalelGr.at(0).getY() + s1_[1] + (aumentarYS1 * pixel));

    ParalelGr.at(2).setX(ParalelGr.at(0).getX() + s2_[0] + (aumentarXS2 * pixel));
    ParalelGr.at(2).setY(ParalelGr.at(0).getY() + s2_[1] * aumentarYS2);

    ParalelGr.at(3).setX(ParalelGr.at(1).getX() + s2_[0] + (aumentarXS2 * pixel));
    ParalelGr.at(3).setY(ParalelGr.at(2).getY() - s1_[1] + (aumentarYS1 * pixel));

    glLineWidth(4.0);
    glEnable(GL_LINE_STIPPLE);
    glLineStipple(1, 0x5555);
    glColor3f(0.50, 0.50, 0.50);
    glBegin(GL_LINES);
    glVertex3f(ParalelGr.at(0).getX(), ParalelGr.at(0).getY(), 0.0);
    glVertex3f(ParalelGr.at(1).getX(), ParalelGr.at(1).getY(), 0.0);

    glVertex3f(ParalelGr.at(0).getX(), ParalelGr.at(0).getY(), 0.0);
    glVertex3f(ParalelGr.at(2).getX(), ParalelGr.at(2).getY(), 0.0);

    glVertex3f(ParalelGr.at(1).getX(), ParalelGr.at(1).getY(), 0.0);
    glVertex3f(ParalelGr.at(3).getX(), ParalelGr.at(3).getY(), 0.0);

    glVertex3f(ParalelGr.at(2).getX(), ParalelGr.at(2).getY(), 0.0);
    glVertex3f(ParalelGr.at(3).getX(), ParalelGr.at(3).getY(), 0.0);
    glEnd();
    glDisable(GL_LINE_STIPPLE);
}

void drawOperations() //Dibuja las operaciones disponibles
{
    glLineWidth(4.0);
    glEnable(GL_LINE_STIPPLE);
    glLineStipple(1, 0x5555);
    //Dibuja la suma de los vectores A y B
    if (isSum)
    {
        glColor3f(1.0, 0.0, 0.0);
        glBegin(GL_LINES);
        glVertex3f(0.0, 0.0, 0.0);
        glVertex3f((distanceX(points.at(0), points.at(1)) * s1.getValue()),
                   (distanceY(points.at(0), points.at(2)) * s2.getValue()),
                   0.0);
        glEnd();
    }
    //Dibuja la resta de los vectores A-B
    if (isSub)
    {
        glColor3f(0.0, 1.0, 0.0);
        glBegin(GL_LINES);
        glVertex3f(ParalelGr.at(1).getX(), ParalelGr.at(1).getY(), 0.0);
        glVertex3f(ParalelGr.at(2).getX(), ParalelGr.at(2).getY(), 0.0);
        glEnd();
    }

    glDisable(GL_LINE_STIPPLE);
}

void drawSliders() //Dibuja los slider para modificar el vector A y el vector B
{
    glColor3f(0.0, 0.0, 1.0);
    s1.drawSlider();
    glRasterPos3f(s1.getSliderX() - 10, s1.getSliderY() + 10, 0.0);
    sprintf(texto, "A = %.1f", s1.getValue());
    escribirTextoBitMap(GLUT_BITMAP_8_BY_13, texto); //Vector A y su valor actual
    glColor3f(1.0, 0.0, 1.0);
    s2.drawSlider();
    glRasterPos3f(s2.getSliderX() - 10, s2.getSliderY() + 10, 0.0);
    sprintf(texto, "B = %.1f", s2.getValue());
    escribirTextoBitMap(GLUT_BITMAP_8_BY_13, texto); //Vector A y su valor actual
}

void drawSliderLines() /*Dibuja los vectores A y B segun 
el valor de su respectivo slider*/
{
    //Dibujado del vector A
    aumentarXS1 = (distanceX(points.at(0), points.at(1)) / pixel) * abs(s1.getValue());
    aumentarYS1 = (distanceY(points.at(0), points.at(1)) / pixel) * abs(s1.getValue());
    if (points.at(1).getX() < points.at(0).getX())
        aumentarXS1 *= -1;
    if (points.at(1).getY() < points.at(0).getY())
        aumentarYS1 *= -1;

    glColor3f(0.0, 0.0, 1.0);
    glLineWidth(3.5);
    glBegin(GL_LINES);
    glVertex2i(0, 0);
    glVertex2i(s1_[0] * aumentarXS1, s1_[1] + (aumentarYS1 * pixel));
    glEnd();

    //Dibujado del vector B
    aumentarXS2 = (distanceX(points.at(0), points.at(2)) / pixel) * abs(s2.getValue());
    aumentarYS2 = (distanceY(points.at(0), points.at(2)) / pixel) * abs(s2.getValue());
    if (points.at(2).getX() < points.at(0).getX())
        aumentarXS2 *= -1;
    if (points.at(2).getY() < points.at(0).getY())
        aumentarYS2 *= -1;

    glColor3f(1.0, 0.0, 1.0);
    glBegin(GL_LINES);
    glVertex2i(0, 0);
    glVertex2i(s2_[0] + (aumentarXS2 * pixel), s2_[1] * aumentarYS2);
    glEnd();
}

void drawLines() //Dibuja los vectores de control U y V
{
    //Dibujado del vector U
    glColor3f(0.0, 0.0, 1.0);
    glLineWidth(3.0);
    glBegin(GL_LINES);
    glVertex2i(points.at(0).getX(), points.at(0).getY());
    glVertex2i(points.at(1).getX(), points.at(1).getY());
    glEnd();

    //Dibujado del vector V
    glColor3f(1.0, 0.0, 1.0);
    glBegin(GL_LINES);
    glVertex2i(points.at(0).getX(), points.at(0).getY());
    glVertex2i(points.at(2).getX(), points.at(2).getY());
    glEnd();
}

void drawAxis(void) //Dibuja los ejes X y Y del Mapa
{
    glColor3f(0.0, 0.0, 0.0);
    //Eje de las X
    glBegin(GL_LINES);
    glVertex2i(-width / 2, 0);
    glVertex2i(width / 2, 0);
    glEnd();
    //Eje de las Y
    glBegin(GL_LINES);
    glVertex2i(0, -height / 2);
    glVertex2i(0, height / 2);
    glEnd();
}

void drawGrid(void) //Dibuja la malla de cuadros del mapa
{
    int i;

    glEnable(GL_LINE_STIPPLE);
    glLineStipple(1, 0x5555);
    glColor3f(0.75, 0.75, 0.75);

    glBegin(GL_LINES);
    //Lineas verticales
    for (i = -9; i <= 9; i++)
    {
        glVertex3f(i * 0.05 * width, height, 0.0);
        glVertex3f(i * 0.05 * width, -height, 0.0);
    }
    //Lineas Horizontales
    for (i = -9; i <= 9; i++)
    {
        glVertex3f(-width * width, i * 0.05 * height, 0.0);
        glVertex3f(width, i * 0.05 * height, 0.0);
    }
    glEnd();
    glDisable(GL_LINE_STIPPLE);
}

void drawScene(void) //Funcion de dibujado principal
{
    glClear(GL_COLOR_BUFFER_BIT);
    glColor3f(0.0, 0.0, 0.0);
    glLineWidth(1.0);
    if (isGrid)
        drawGrid();
    if (isAxis)
        drawAxis();
    if (isP)
        drawP();
    if (isRule)
        drawParalelogramo();
    drawLines();
    drawPoints();
    glColor3f(0.0, 0.0, 0.0);
    O.drawPoint();
    drawSliders();
    drawOperations();
    drawSliderLines();
    glutSwapBuffers();
}

void PassiveMouseS2(int x, int y)
{
    tempX = -width / 2 + width * x / width;
    s2_[1] = 0;
    s2_[1] = s2_[1] + s2.getValue() * pixel;

    s2.setSliderX(tempX);
    glutPostRedisplay();
}

void PassiveMouseS1(int x, int y)
{
    tempX = -width / 2 + width * x / width;
    s1_[0] = 0;
    s1_[0] = s1_[0] + s1.getValue() * pixel;
    s1.setSliderX(tempX);
    glutPostRedisplay();
}
void PassiveMousePoints(int x, int y) /*Funcion para mover los puntos 
una vez dado click en ellos*/
{
    tempX = -width / 2 + width * x / width;
    tempY = height / 2 - height * y / height;

    CP->setX(tempX);
    CP->setY(tempY);
    glutPostRedisplay();
}

void mouseCallBack(int btn, int state, int x, int y)
{

    if (btn == GLUT_LEFT_BUTTON && state == GLUT_DOWN && CP == NULL)
    {
        pointsIterator = points.begin();
        x = x - width / 2;
        y = height / 2 - y;
        int i = 0;

        if (inRange(O.getX() - pointSize, O.getX() + pointSize, x) &&
            inRange(O.getY() - pointSize, O.getY() + pointSize, y))
        {
            CP = &O;
            glutPassiveMotionFunc(PassiveMousePoints);
            return;
        }

        if (inRange(P.getX() - pointSize, P.getX() + pointSize, x) &&
            inRange(P.getY() - pointSize, P.getY() + pointSize, y))
        {
            CP = &P;
            glutPassiveMotionFunc(PassiveMousePoints);
            return;
        }

        if (inRange(s1.getSliderX() - pointSize, s1.getSliderX() + pointSize, x) &&
            inRange(s1.getSliderY() - pointSize, s1.getSliderY() + pointSize, y))
        {
            CP = &points.at(0);
            glutPassiveMotionFunc(PassiveMouseS1);
            return;
        }

        if (inRange(s2.getSliderX() - pointSize, s2.getSliderX() + pointSize, x) &&
            inRange(s2.getSliderY() - pointSize, s2.getSliderY() + pointSize, y))
        {
            CP = &points.at(0);
            glutPassiveMotionFunc(PassiveMouseS2);
            return;
        }
        while (pointsIterator != points.end())
        {

            if (inRange(pointsIterator->getX() - pointSize, pointsIterator->getX() + pointSize, x) &&
                inRange(pointsIterator->getY() - pointSize, pointsIterator->getY() + pointSize, y))
            {
                CP = &points.at(i);
                glutPassiveMotionFunc(PassiveMousePoints);
            }
            pointsIterator++;
            i++;
        }
        return;
    }
    if (btn == GLUT_LEFT_BUTTON && state == GLUT_DOWN && CP != NULL)
    {
        CP = NULL;
        glutPassiveMotionFunc(NULL);
        glutPostRedisplay();
    }

    if (btn == GLUT_RIGHT_BUTTON && state == GLUT_DOWN)
        exit(0);
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
    makeMenu();
    //PUNTOS INICIALES
    Point p0 = Point(-6 * pixel, 0);
    points.push_back(p0);
    //Punto U
    Point p1 = Point(-5 * pixel, 0);
    points.push_back(p1);
    //Punto V
    Point p2 = Point(-6 * pixel, pixel);
    points.push_back(p2);
}
// Routine to output interaction instructions to the C++ window.
void printInteraction(void)
{
    cout << "Interaction:" << endl;
    cout << "Left click on a box on the left to select a primitive." << endl
         << "Then left click on the drawing area: once for point, twice for line or rectangle." << endl
         << "Right click for menu options." << endl;
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
    glutCreateWindow("canvas.cpp");
    glutDisplayFunc(drawScene);
    glutReshapeFunc(resize);
    glutKeyboardFunc(keyInput);
    glutMouseFunc(mouseCallBack);

    glewExperimental = GL_TRUE;
    glewInit();

    setup();

    glutMainLoop();
}
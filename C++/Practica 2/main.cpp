#include "core/text.h"
#include "core/point.h"
#include "core/slider.h"
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
//Variables de opciones
static int isGrid = 1;
static int isAxis = 1;
static int isRule = 1;
static int isSub = 1;
static int isSum = 1;
static int isP = 1;
static float pixel = 30;                      //Tamaño de cada cuadro del mapa
static long font = (long)GLUT_BITMAP_8_BY_13; // Font selection.
int sliding = 0;
float s1_[2] = {0, 0};
float s2_[2] = {0, 0};
Point *CP = NULL;
Point P = Point(-pixel, 4 * pixel);
Point O = Point(0, 0);
vector<Point> ParalelGr{Point(0, 0), Point(0, 0), Point(0, 0), Point(0, 0), Point(0, 0)};
static Slider s1 = Slider(8 * pixel, 9 * pixel, 10);
static Slider s2 = Slider(8 * pixel, 8 * pixel, 10);

float distanceX(Point p0, Point p1)
{
    return abs(sqrt(pow(p0.getX() - p1.getX(), 2)));
}

float distanceY(Point p0, Point p1)
{
    return abs(sqrt(pow(p0.getY() - p1.getY(), 2)));
}

void drawP()
{
    glPushMatrix();
    glColor3f(0.0, 0.0, 0.0);
    glBegin(GL_LINES);
    glVertex2i(O.getX(), O.getY());
    glVertex2i(P.getX(), P.getY());
    glEnd();
    P.drawPoint();
    glPopMatrix();
}

void drawParalelogramo()
{
    ParalelGr.at(0).setX(O.getX());
    ParalelGr.at(0).setY(O.getY());

    ParalelGr.at(1).setX(ParalelGr.at(0).getX() + s1_[0] * aumentarXS1);
    ParalelGr.at(1).setY(ParalelGr.at(0).getY() + s1_[1] + (aumentarYS1 * pixel));

    ParalelGr.at(2).setX(ParalelGr.at(0).getX() + s2_[0] + (aumentarXS2 * pixel));
    ParalelGr.at(2).setY(ParalelGr.at(0).getY() + s2_[1] * aumentarYS2);

    ParalelGr.at(3).setX(ParalelGr.at(1).getX()+ParalelGr.at(2).getX());
    ParalelGr.at(3).setY(ParalelGr.at(2).getY());

    ParalelGr.at(4).setX((s1_[0] * aumentarXS1) + (s2_[0] + (aumentarXS2 * pixel)));
    ParalelGr.at(4).setY(s2_[1] * aumentarYS2);

    glPushMatrix();
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
    glPopMatrix();
}

void drawOperations()
{
    glPushMatrix();
    glLineWidth(4.0);
    glEnable(GL_LINE_STIPPLE);
    glLineStipple(1, 0x5555);

    if (isSum)
    {
        glColor3f(1.0, 0.0, 0.0);
        glBegin(GL_LINES);
        glVertex3f(0.0, 0.0, 0.0);
        glVertex3f(ParalelGr.at(4).getX(), ParalelGr.at(4).getY(), 0.0);
        glEnd();
    }

    if (isSub)
    {
        glColor3f(0.0, 1.0, 0.0);
        glBegin(GL_LINES);
        glVertex3f(ParalelGr.at(1).getX(), ParalelGr.at(1).getY(), 0.0);
        glVertex3f(ParalelGr.at(2).getX(), ParalelGr.at(2).getY(), 0.0);
        glEnd();
    }

    glDisable(GL_LINE_STIPPLE);
    glPopMatrix();
}

bool inRange(unsigned low, unsigned high, unsigned x)
{
    return ((x - low) <= (high - low));
}

void drawSliders()
{
    glPushMatrix();
    glColor3f(0.0, 0.0, 1.0);
    s1.drawSlider();
    glColor3f(1.0, 0.0, 1.0);
    s2.drawSlider();
    glPopMatrix();
}

void drawSliderLines()
{

    aumentarXS1 = (distanceX(points.at(0), points.at(1)) / pixel) * abs(s1.getValue());
    aumentarYS1 = (distanceY(points.at(0), points.at(1)) / pixel) * abs(s1.getValue());
    if (points.at(1).getX() < points.at(0).getX())
        aumentarXS1 *= -1;
    if (points.at(1).getY() < points.at(0).getY())
        aumentarYS1 *= -1;
    //cout << "AumentarX: " << aumentarXS1 << endl;
    //cout << "AumentarY: " << aumentarYS1 << endl;
    //cout << "BlueValue: " << s1.getValue() << endl;
    glColor3f(0.0, 0.0, 1.0);
    glLineWidth(3.5);
    glBegin(GL_LINES);
    glVertex2i(0, 0);
    glVertex2i(s1_[0] * aumentarXS1, s1_[1] + (aumentarYS1 * pixel));
    glEnd();
    //cout << "Blue \t X: " << s1_[0] << "\tY: " << s1_[1] << endl;

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
    //cout << "Magenta \t X: " << s2_[0] << "\tY: " << s2_[1] << endl;
}

void drawLines()
{
    glPushMatrix();
    glColor3f(0.0, 0.0, 1.0);
    glLineWidth(3.0);
    glBegin(GL_LINES);
    glVertex2i(points.at(0).getX(), points.at(0).getY());
    glVertex2i(points.at(1).getX(), points.at(1).getY());
    glEnd();
    //cout << "BlueLine \t X: " << points.at(1).getX() << "\tY: " << points.at(1).getY() << endl;

    glColor3f(1.0, 0.0, 1.0);
    glBegin(GL_LINES);
    glVertex2i(points.at(0).getX(), points.at(0).getY());
    glVertex2i(points.at(2).getX(), points.at(2).getY());
    glEnd();
    //cout << "MagentaLine \t X: " << points.at(2).getX() << "\tY: " << points.at(2).getY() << endl;
    glPopMatrix();
}

void drawAxis(void)
{
    glPushMatrix();
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

// Function to draw a grid.
void drawGrid(void)
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

// Drawing routine.
void drawScene(void)
{
    glClear(GL_COLOR_BUFFER_BIT);
    glColor3f(0.0, 0.0, 0.0);
    glLineWidth(1.0);
    if (isGrid)
        drawGrid();
    if (isAxis)
        drawAxis();
    drawLines();
    drawPoints();
    glPushMatrix();
    glColor3f(0.0, 0.0, 0.0);
    O.drawPoint();
    glPopMatrix();
    drawSliders();
    if (isP)
        drawP();
    if (isRule)
        drawParalelogramo();
    drawOperations();
    drawSliderLines();
    glutSwapBuffers();
}

void slider2MouseMove(int x, int y)
{
    //cout << "X: " << x << endl;
    //cout << "x: " << x << endl;
    tempX = -width / 2 + width * x / width;
    s2_[1] = 0;
    s2_[1] = s2_[1] + s2.getValue() * pixel;

    s2.setSliderX(tempX);
    glutPostRedisplay();
}

void slider1MouseMove(int x, int y)
{
    tempX = -width / 2 + width * x / width;
    s1_[0] = 0;
    cout << "Value: " << s1.getValue() << endl;
    s1_[0] = s1_[0] + s1.getValue() * pixel;
    s1.setSliderX(tempX);
    glutPostRedisplay();
}
void myMouseMove(int x, int y)
{
    //cout << "X: " << x << endl;
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
        //cout << "PUNTO" << currentPoint.getX();
        pointsIterator = points.begin();
        //printf("Mouse call back: button=%d, state=%d, x=%d, y=%d\n", btn, state, x, y);
        x = x - width / 2;
        y = height / 2 - y;
        int i = 0;

        if (inRange(O.getX() - pointSize, O.getX() + pointSize, x) &&
            inRange(O.getY() - pointSize, O.getY() + pointSize, y))
        {
            CP = &O;
            glutPassiveMotionFunc(myMouseMove);
            return;
        }

        if (inRange(P.getX() - pointSize, P.getX() + pointSize, x) &&
            inRange(P.getY() - pointSize, P.getY() + pointSize, y))
        {
            CP = &P;
            glutPassiveMotionFunc(myMouseMove);
            return;
        }

        if (inRange(s1.getSliderX() - pointSize, s1.getSliderX() + pointSize, x) &&
            inRange(s1.getSliderY() - pointSize, s1.getSliderY() + pointSize, y))
        {
            cout << "Slider" << endl;
            CP = &points.at(0);
            glutPassiveMotionFunc(slider1MouseMove);
            return;
        }

        if (inRange(s2.getSliderX() - pointSize, s2.getSliderX() + pointSize, x) &&
            inRange(s2.getSliderY() - pointSize, s2.getSliderY() + pointSize, y))
        {
            cout << "Slider2" << endl;
            CP = &points.at(0);
            glutPassiveMotionFunc(slider2MouseMove);
            return;
        }
        while (pointsIterator != points.end())
        {
            //cout << "Punto X: " << pointsIterator->getX() << ", Punto Y: " << pointsIterator->getY() << endl;

            if (inRange(pointsIterator->getX() - pointSize, pointsIterator->getX() + pointSize, x) &&
                inRange(pointsIterator->getY() - pointSize, pointsIterator->getY() + pointSize, y))
            {
                CP = &points.at(i);
                glutPassiveMotionFunc(myMouseMove);
            }
            pointsIterator++;
            i++;
        }
        return;
    }
    if (btn == GLUT_LEFT_BUTTON && state == GLUT_DOWN && CP != NULL)
    {
        cout << "Entro 2" << endl;
        CP = NULL;
        sliding = 0;
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

void rightMenu(int id)
{
    if (id == 1)
    {
        glutPostRedisplay();
    }
    if (id == 2)
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

    glutCreateMenu(rightMenu);
    glutAddSubMenu("Grid", sub_menu);
    glutAddSubMenu("Axis", sub_menu2);

    glutAddMenuEntry("Clear", 1);
    glutAddMenuEntry("Quit", 2);
    glutAttachMenu(GLUT_RIGHT_BUTTON);
}

// Initialization routine.
void setup(void)
{
    glClearColor(1.0, 1.0, 1.0, 0.0);
    makeMenu();
    Point p0 = Point(-6 * pixel, 0);
    points.push_back(p0);
    Point p1 = Point(-5 * pixel, 0);
    points.push_back(p1);
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
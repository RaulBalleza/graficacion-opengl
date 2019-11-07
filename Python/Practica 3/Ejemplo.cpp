/////////////////////////////////////////////////////////////////////
// circle.cpp
//
// This program draws a line loop with vertices equally apart on
// a fixed circle. The larger the number of vertices the better
// the loop approximates the circle.
//
// Interaction:
// Press +/- to increase/decrease the number of vertices of the loop.
//
// Sumanta Guha.
/////////////////////////////////////////////////////////////////////

#include <cstdlib>
#include <cmath>
#include <iostream>

#ifdef __APPLE__
#include <GLUT/glut.h>
#else
#include <GL/glut.h>
#endif

#define AlturaVentana 480
#define AnchuraVentana 640
#define PI 3.14159265358979324
int tamano = 50;

float moveX = 0;
float moveY = 0;

float angulo = 0;
float anguloT = 0;
int tipo = 0, tipo2 = 0;
double velocidad = 0.4;
bool bandera = false;

//Lineas verticales
double linea1_1 = -100;
double linea1_2 = -110;
double linea2_1 = 100;
double linea2_2 = 110;

//Lineas Horizontales
double linea3_1 = -100;
double linea3_2 = -110;
double linea4_1 = 100;
double linea4_2 = 110;

//Lineas diagonales
double linea5_x1 = 0;
double linea5_x2 = 0;
double linea5_y1 = 0;
double linea5_y2 = 0;

double linea6_x1 = 0;
double linea6_x2 = 0;
double linea6_y1 = 0;
double linea6_y2 = 0;

// Globals.
static float R = (tamano / 2) + 10; // Radius of circle.
static float X = 00.0;				// X-coordinate of center of circle.
static float Y = -tamano / 2;		// Y-coordinate of center of circle.
static int numVertices = 40;		// Number of vertices on circle.

using namespace std;

void buscarLineas()
{
	int resultado = 0;
	double resultado2 = 0;
	int multiplicador = 0;
	while (resultado < 100)
	{
		multiplicador++;
		resultado2 += tamano / 2;
		resultado = tamano * multiplicador;
	}
	linea5_x1 = resultado2;
	linea5_x2 = resultado2;
	linea5_y1 = resultado;
	linea5_y2 = resultado;

	linea6_x1 = -resultado2;
	linea6_x2 = -resultado2;
	linea6_y1 = resultado;
	linea6_y2 = resultado;
}

void dibujarCirculo(void)
{
	float t = 0; // Angle parameter.
	int i;
	glBegin(GL_LINE_LOOP);
	for (i = 0; i < numVertices; ++i)
	{
		//glColor3ub(0,0,0);
		glVertex3f(X + R * cos(t), Y + R * sin(t), 0.0);
		t += 2 * PI / numVertices;
	}
	glEnd();
}

void dibujarCuadro(void)
{
	glBegin(GL_LINE_LOOP);
	glVertex3f(-tamano / 2, 0, 0.0);
	glVertex3f(tamano / 2, 0, 0.0);
	glVertex3f(tamano / 2, -tamano, 0);
	glVertex3f(-tamano / 2, -tamano, 0);
	glEnd();
}

void dibujarTrinangulo(void)
{
	glBegin(GL_LINE_LOOP);
	glVertex3f(-tamano / 2, -tamano, 0.0);
	glVertex3f(0, 0, 0.0);
	glVertex3f(tamano / 2, -tamano, 0);
	glVertex3f(-tamano / 2, -tamano, 0);
	glEnd();
}

void lineasACuadro(void)
{
	//Lineas verticales
	//Linea 1
	glBegin(GL_LINES);
	glVertex3f(-tamano / 2, linea1_1, 0.0);
	glVertex3f(-tamano / 2, linea1_2, 0.0);
	glEnd();

	//Linea 2
	glBegin(GL_LINES);
	glVertex3f(tamano / 2, linea2_1, 0.0);
	glVertex3f(tamano / 2, linea2_2, 0.0);
	glEnd();

	//Lineas Horizontales
	//Lineas 1
	glBegin(GL_LINES);
	glVertex3f(linea3_1, 0, 0.0);
	glVertex3f(linea3_2, 0, 0.0);
	glEnd();

	glBegin(GL_LINES);
	glVertex3f(linea4_1, -tamano, 0.0);
	glVertex3f(linea4_2, -tamano, 0.0);
	glEnd();
}

void drawRightHalfCircle() // the empty one
{
	glColor3f(0.0, 0.0, 0.0);
	float twoPI = 2 * PI;
	float radius = R;
	glBegin(GL_LINE_LOOP);
	for (float i = 0.0; i <= twoPI / 2; i += 0.001)
		glVertex2f(X + (sin(i) * radius), Y + (cos(i) * radius));

	glEnd();
}

void lineasATriangulo(void)
{
	//De derecha a izquierda
	glBegin(GL_LINES);
	glVertex3f(linea5_x1, -1 * linea5_y1, 0.0);
	glVertex3f(linea5_x2, -1 * linea5_y2, 0.0);
	glEnd();

	//Linea de izquierda a derecha
	glBegin(GL_LINES);
	glVertex3f(linea6_x1, -1 * linea6_y1, 0.0);
	glVertex3f(linea6_x2, -1 * linea6_y2, 0.0);
	glEnd();
}

void drawHalfs()
{
	glPushMatrix();
	glTranslatef(angulo, angulo, 0);
	glRotatef(-angulo, 0, 0, 1);
	//DERECHA
	glPushMatrix();
	glScalef(0.25, 0.72, 1);
	glTranslatef(100, -9, 0);
	drawRightHalfCircle();
	glPopMatrix();
	glPopMatrix();

	//IZQUIERDA
	glPushMatrix();
	glTranslatef(-angulo, -angulo, 0);
	glRotatef(-angulo, 0, 0, 1);
	glPushMatrix();
	glScalef(0.25, 0.72, 1);
	glTranslatef(-100, -9, 0);
	glRotatef(180, 0, 1, 0);
	drawRightHalfCircle();
	glPopMatrix();
	glPopMatrix();

	//ARRIBA
	glPushMatrix();
	glTranslatef(-angulo, angulo, 0);
	glRotatef(-angulo, 0, 0, 1);
	glPushMatrix();
	glScalef(0.72, 0.25, 1);
	glTranslatef(-25, 0, 0);
	glRotatef(90, 0, 0, 1);
	drawRightHalfCircle();
	glPopMatrix();
	glPopMatrix();

	//ABAJO
	glPushMatrix();
	glTranslatef(angulo, -angulo, 0);
	glRotatef(-angulo, 0, 0, 1);
	glPushMatrix();
	glScalef(0.72, 0.25, 1);
	glTranslatef(25, -198, 0);
	glRotatef(-90, 0, 0, 1);
	drawRightHalfCircle();
	glPopMatrix();
	glPopMatrix();
}

void drawTriangles()
{
	glPushMatrix();
	glTranslatef(anguloT, anguloT, 0);
	glRotatef(-anguloT, 0, 0, 1);
	glBegin(GL_LINE_LOOP);
	glVertex3f(0, 0, 0.0);
	glVertex3f(25, 0, 0.0);
	glVertex3f(25, -50, 0.0);
	glEnd();
	glPopMatrix();

	glPushMatrix();
	glTranslatef(-anguloT, anguloT, 0);
	glRotatef(-anguloT, 0, 0, 1);
	glBegin(GL_LINE_LOOP);
	glVertex3f(0, 0, 0.0);
	glVertex3f(-25, 0, 0.0);
	glVertex3f(-25, -50, 0.0);
	glEnd();
	glPopMatrix();
}

// Drawing routine.
void displayMe(void)
{
	glClear(GL_COLOR_BUFFER_BIT);

	glPointSize(10);
	glBegin(GL_POINTS);
	glVertex3f(moveX, moveY, 0.0);
	glEnd();
	glColor3f(0.0, 0.0, 0.0);
	cout << "X: " << moveX << endl;
	cout << "Y: " << moveY << endl;
	if (tipo2 == 0)
	{
		angulo = 0;
		dibujarCirculo();
	}
	else
	{
		if (tipo2 == 1)
		{
			drawHalfs();
			dibujarCuadro();
			angulo += 1.0;
		}
		else
		{
			if (tipo2 == 2)
			{
				dibujarTrinangulo();
				drawTriangles();
				anguloT += 0.7;
			}
		}
	}

	lineasACuadro();
	lineasATriangulo();
	glFlush();
}

// Initialization routine.
void init(void)
{
	glClearColor(1.0, 1.0, 1.0, 0.0);
}

// OpenGL window reshape routine.
void resize(int w, int h)
{
	glViewport(0, 0, (GLsizei)w, (GLsizei)h);
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	//glOrtho(0.0, 100.0, 0.0, 100.0, -1.0, 1.0);
	glOrtho(-100.0, 100.0, -100.0, 100.0, -1.0, 1.0);
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
	case 'X':
		moveX += 1.0;
		break;
	case 'x':
		moveX -= 1.0;
		break;
	case 'Y':
		moveY += 1.0;
		break;
	case 'y':
		moveY -= 1.0;
		break;
	default:
		break;
	}
}

// Routine to output interaction instructions to the C++ window.
void printInteraction(void)
{
	cout << "Interaction:" << endl;
	cout << "Press +/- to increase/decrease the number of vertices on the circle." << endl;
	cout << "Press [ESCAPE] to finish." << endl;
}

void ciclo()
{
	if (tipo == 0)
	{ //Se convierte a cuadrado
		//Linea 1 vertical
		if (linea1_1 <= 100)
		{
			linea1_1 += velocidad; //Linea vertical
			linea3_1 += velocidad; //Linea horizontal
		}
		else
		{
			if (linea1_2 <= 100)
			{
				linea1_2 += velocidad; //Linea vertical
				linea3_2 += velocidad; //Linea horizontal
			}
			else
			{
				linea1_1 = -100; //Linea vertical
				linea1_2 = -110; //Linea vertical
				linea3_1 = -100; //Linea horizontal
				linea3_2 = -110; //Linea horizontal
			}
		}

		if (linea1_1 >= 20 && bandera == false)
		{
			glLoadIdentity();
			tipo2 = 1;
			bandera = true;
		}

		//Linea 2 vertical y 4 horizontal
		if (linea2_1 >= -100)
		{
			linea2_1 -= velocidad; //Linea vertical
			linea4_1 -= velocidad; //Linea horizontal
		}
		else
		{
			if (linea2_2 >= -100)
			{
				linea2_2 -= velocidad; //Linea vertical
				linea4_2 -= velocidad; //Linea horizontal
			}
			else
			{
				linea2_1 = 100; //Linea vertical
				linea2_2 = 110; //Linea vertical
				linea4_1 = 100; //Linea horizontal
				linea4_2 = 110; //Linea horizontal
				tipo = 1;		//Cambio a lineas de triangulo
				glLoadIdentity();
				bandera = false;
				buscarLineas();
			}
		}
	}
	else
	{
		if (tipo == 1)
		{ //Lineas de triangulo
			if (linea5_x1 >= -100)
			{
				linea5_x1 -= velocidad;
				linea5_y1 -= velocidad * 2;
			}
			else
			{
				if (linea5_x2 >= -100)
				{
					linea5_x2 -= velocidad;
					linea5_y2 -= velocidad * 2;
				}
			}

			if (linea6_x1 <= 100)
			{
				linea6_x1 += velocidad;
				linea6_y1 -= velocidad * 2;
			}
			else
			{
				if (linea6_x2 <= 100)
				{
					linea6_x2 += velocidad;
					linea6_y2 -= velocidad * 2;
				}
			}

			if (-1 * linea5_y1 >= 15 && bandera == false)
			{
				glLoadIdentity();
				tipo2 = 2;

				bandera = true;
			}

			if (-1 * linea5_y2 >= 100)
			{
				tipo = 0;
				tipo2 = 0;
				bandera = false;
			}
		}
	}

	//Actualizador
	glutPostRedisplay();
}

// Main routine.
int main(int argc, char **argv)
{
	printInteraction();
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
	glutInitWindowSize(AnchuraVentana, AlturaVentana);
	glutCreateWindow("Circles.gif");
	init();
	glutDisplayFunc(displayMe);
	glutReshapeFunc(resize);
	glutKeyboardFunc(keyInput);
	glutIdleFunc(ciclo);
	glutMainLoop();

	return 0;
}
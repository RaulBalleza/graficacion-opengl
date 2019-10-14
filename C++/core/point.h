#include "librerias.h"
using namespace std;
static float pointSize = 8.0; // Size of point

// Point class.
class Point
{
public:
    Point(int xVal, int yVal)
    {
        x = xVal;
        y = yVal;
    }
    void drawPoint(void); // Function to draw a point.
    int getX(void);
    int getY(void);
    void setX(int x_);
    void setY(int y_);

private:
    int x, y;          // x and y co-ordinates of point.
    static float size; // Size of point.
};

float Point::size = pointSize; // Set point size.

// Function to draw a point.
void Point::drawPoint()
{
    glPointSize(size);
    glBegin(GL_POINTS);
    glVertex3f(x, y, 0.0);
    glEnd();
}

int Point::getX()
{
    return x;
}

int Point::getY()
{
    return y;
}

void Point::setX(int x_)
{
    x = x_;
}

void Point::setY(int y_)
{
    y = y_;
}

// Vector of points.
vector<Point> points;

// Iterator to traverse a Point array.
vector<Point>::iterator pointsIterator;

// Function to draw all points in the points array.
void drawPoints(void)
{
    // Loop through the points array drawing each point.
    glPushMatrix();
    glColor3f(1.0, 0.0, 0.0);
    pointsIterator = points.begin();
    while (pointsIterator != points.end())
    {
        pointsIterator->drawPoint();
        pointsIterator++;
    }
    glPopMatrix();
}
#include "librerias.h"
class Slider
{
public:
    Slider(int x_, int y_, int units_)
    {
        x = x_;
        y = y_;
        sliderx = x;
        slidery = y;
        min = -units_;
        max = units_;
        value = 0;
    }

    void drawSlider(void);
    void drawBar(void);
    float getSliderX();
    float getSliderY();
    void setSliderX(float);
    float getValue();

private:
    int x, y, min, max;
    float sliderx, slidery, value;
    Point slider = Point(0, 0);
};

float Slider::getValue()
{
    return value;
}

float Slider::getSliderX()
{
    return sliderx;
}

float Slider::getSliderY()
{
    return slidery;
}

void Slider::setSliderX(float x_)
{
    //cout<<"x_"<<x_<<endl;
    sliderx = x_;
    value = sliderx - x;
    //cout<<"Value: "<<value<<endl;
    if (sliderx > x + max)
    {
        sliderx = x + max;
        //cout << "sliderX: " << sliderx << endl;
    }
    else
    {
        if (sliderx < x + min)
        {
            sliderx = x + min;
            //cout << "sliderX: " << sliderx << endl;
        }
    }
}

void Slider::drawBar()
{
    glLineWidth(2.0);
    glBegin(GL_LINES);
    glVertex2i(x + min * 3, y);
    glVertex2i(x + max * 3, y);
    glEnd();
}

void Slider::drawSlider()
{
    slider.setX(sliderx);
    slider.setY(slidery);
    slider.drawPoint();
    drawBar();
}

#include "librerias.h"
void escribirTextoBitMap(void *font, char *string)
{
    char *c;
    for (c = string; *c != '\0'; c++)
        glutBitmapCharacter(font, *c);
}
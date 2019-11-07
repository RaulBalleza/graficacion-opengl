NombreProgramaFuente=main

rm $NombreProgramaFuente
code $NombreProgramaFuente.cpp
g++ $NombreProgramaFuente.cpp -o $NombreProgramaFuente -lGL -lglut -lGLEW -lGLU -lm
./$NombreProgramaFuente

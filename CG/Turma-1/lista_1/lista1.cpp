#include <math.h>
#include <stdio.h>
#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/glut.h>


#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif


void reshape(GLint width, GLint height);
void display();

void sol();
void circulo(GLfloat raio, GLint n);
void circunferencia(GLfloat raio, GLint n);

// Main 
int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB);
    glutInitWindowSize(800, 800);
    glutInitWindowPosition(100, 100);
   
    glutCreateWindow("Lista 1 - SOL");
    glClearColor(0, 0, 0, 1.0);
    
    glutDisplayFunc(display);
    glutReshapeFunc(reshape);
    glutMainLoop(); 

    return 0;
}


void display() {
    glClear(GL_COLOR_BUFFER_BIT);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    glTranslatef(0.4, 0.4, 0);
    glScalef(0.2, 0.2, 1);
    sol();

    glFlush();
    glutSwapBuffers(); 
}


void reshape(GLint width, GLint height) {
    glViewport(0, 0, width, height);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();

    gluOrtho2D(0, 2, 0, 2);
    
    glMatrixMode(GL_MODELVIEW);
    glutPostRedisplay();
}


void sol() {
    glColor3f(1.0, 0.75, 0.0);
    glLineWidth(2.0);
    
    // Raios do sol
    glBegin(GL_LINES);
    for (int i = 0; i < 12; i++) {
        glVertex2f(0.0, 0.0);
        glVertex2f(1.3 * sin((2 * M_PI / 12) * i), 1.3 * cos((2 * M_PI / 12) * i));
    }
    glEnd();

    // Sol
    glColor3f(1.0, 1.0, 0.5); 
    circulo(1.0, 100);

    // Contorno
    glColor3f(1.0, 0.75, 0.0); 
    glLineWidth(5.0);
    circunferencia(1.0, 100);
    glLineWidth(1.0); 
}

void circulo(GLfloat raio, GLint n) {
    glBegin(GL_POLYGON);
    for (int i = 0; i < n; i++) {
        glVertex2f(raio * sin((2 * M_PI / n) * i), raio * cos((2 * M_PI / n) * i));
    }
    glEnd();
}

void circunferencia(GLfloat raio, GLint n) {
    glBegin(GL_LINE_LOOP);
    for (int i = 0; i < n; i++) {
        glVertex2f(raio * sin((2 * M_PI / n) * i), raio * cos((2 * M_PI / n) * i));
    }
    glEnd();
}
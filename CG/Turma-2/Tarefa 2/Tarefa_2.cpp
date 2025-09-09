#include <GL/glut.h>
#include <stdio.h>
#include <math.h>

int frameCounter;


void display(int);
void frameClock(int valor);

void quadrado(GLfloat x, GLfloat y, GLfloat z, GLfloat size);
void retangulo(GLfloat x, GLfloat y, GLfloat z, GLfloat height, GLfloat width);
void triangulo(GLfloat x, GLfloat y, GLfloat z, GLfloat height, GLfloat base);
void circulo(GLint n);
void circunferencia(GLint n);
void helice();
void roda();

void carro(int n);
void background();
void moinho(int n);
void sol();

int main(int argc, char** argv){
    glutInit(&argc,argv);
    glutInitDisplayMode (GLUT_DOUBLE | GLUT_RGB);

    glutInitWindowSize (1000, 800);
    glutInitWindowPosition (200, 200);

    glutCreateWindow ("Tarefa 1 - Parte 1");

    // Estado Inicial
    glClearColor(0.5,0.8,1,1);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(-10,10,-8,8,-1,1);

    // desenho
    frameClock(frameCounter);

    glutMainLoop();

    return 0;
}


void display(int n){
    glClear(GL_COLOR_BUFFER_BIT);

    background();

    glPushMatrix();
        glTranslatef(8,6,0);
        glRotatef(-0.6*n,0,0,1);
        sol();
    glPopMatrix();

    glPushMatrix();
        glTranslatef(-9,-0.5,0);
        glScalef(2,2,1);
        moinho(1.4*n);
    glPopMatrix();

    glPushMatrix();
        glTranslatef(-5,0,0);
        glScalef(1.2,1.2,1);
        moinho(1.1*n);
    glPopMatrix();
    
    glPushMatrix();
        glTranslatef(0.5,-1,0);
        glScalef(2.3,2.3,1);
        moinho(2*n);
    glPopMatrix();

    glPushMatrix();
        glTranslatef((0.05*n-8),-4.6,0);
        carro(n);
    glPopMatrix();

    glFlush();
    glutSwapBuffers();
}


void frameClock(int valor){
    display(valor);
    valor++;

    glutTimerFunc(10,frameClock,valor);
}


void quadrado(GLfloat x, GLfloat y, GLfloat z, GLfloat size){
    float s = size/2;
    
    glBegin(GL_QUADS);
        glVertex3f(x-s,y+s,z);
        glVertex3f(x+s,y+s,z);
        glVertex3f(x+s,y-s,z);
        glVertex3f(x-s,y-s,z);
    glEnd();
}


void retangulo(GLfloat x, GLfloat y, GLfloat z, GLfloat height, GLfloat width){
    float h = height/2;
    float w = width/2;
    
    glBegin(GL_QUADS);
        glVertex3f(x-w,y+h,z);
        glVertex3f(x+w,y+h,z);
        glVertex3f(x+w,y-h,z);
        glVertex3f(x-w,y-h,z);
    glEnd();
}


void triangulo(GLfloat x, GLfloat y, GLfloat z, GLfloat height, GLfloat base){
    float b = base/2;

    glBegin(GL_TRIANGLES);
        glVertex3f(x-b,y,z);
        glVertex3f(x,y+height,z);
        glVertex3f(x+b,y,z);
    glEnd();
}


void helice(){
    glColor3f(0.8,0.3,0.3);

    glBegin(GL_POLYGON);
        glVertex3f(0,0,0);
        glVertex3f(0.25,0.1,0);
        glVertex3f(1,0,0);
        glVertex3f(0.25,-0.1,0);
    glEnd();
}


void circulo(GLint n){
    glBegin(GL_POLYGON);
        for (int i=0; i<n; i++) {glVertex3f(sin((2*M_PI/n)*i),cos((2*M_PI/n)*i),0);}
    glEnd();
}


void circunferencia(GLint n){
    glBegin(GL_LINE_LOOP);
        for (int i=0; i<n; i++) {glVertex3f(sin((2*M_PI/n)*i),cos((2*M_PI/n)*i),0);}
    glEnd();
}


void roda(){
    glColor3f(0.5,0.5,0.5);

    circulo(100);

    glColor3f(0,0,0);
    glBegin(GL_LINES);
        for (int i=0; i<12; i++) {
            glVertex3f(0,0,0);
            glVertex3f(sin((2*3.1415/12)*i),cos((2*3.1415/12)*i),0);
        }
    glEnd();

    glLineWidth(5);
    circunferencia(100);
    glLineWidth(1);
}


void carro(int n){

    glPushMatrix();
    glTranslatef(-0.75,-0.3,0);
    glScalef(0.3,0.3,1);
    glRotatef(-n,0,0,1);
    roda();
    glPopMatrix();
    
    glPushMatrix();
    glTranslatef(0.75,-0.3,0);
    glScalef(0.3,0.3,1);
    glRotatef(-n,0,0,1);
    roda();
    glPopMatrix();

    glColor3f(1,0,0);
    retangulo(0,0.5,0,1,3);
    retangulo(-0.4,1.25,0,0.5,1);
}


void moinho(int n){
    glColor3f(0.4,0.4,0.4);
    retangulo(0,1,0,2,0.1);

    glPushMatrix();
    glTranslatef(0,2,0);
    glRotatef(n,0,0,1);
    helice();
    glPushMatrix();
    glRotated(120,0,0,1);
    helice();
    glPushMatrix();
    glRotated(120,0,0,1);
    helice();
    glPopMatrix();
    glPopMatrix();
    glPopMatrix();

    glPushMatrix();
    glTranslatef(0,2,0);
    glScalef(0.1,0.1,1);
    circulo(50);
    glPopMatrix();
}


void sol(){
    glColor3f(1,1,0.5);

    glColor3f(1,0.75,0);
    glBegin(GL_LINES);
        for (int i=0; i<12; i++) {
            glVertex3f(0,0,0);
            glVertex3f(1.3*sin((2*3.1415/12)*i),1.3*cos((2*3.1415/12)*i),0);
        }
    glEnd();

    circulo(100);

    glLineWidth(5);
    circunferencia(100);
    glLineWidth(1);
}


void background(){
    glColor3f(0,1,0);
    glBegin(GL_POLYGON);
        glVertex3f(-10,-8,0);
        glVertex3f(-10,-1,0);
        glVertex3f(-7,1,0);
        glVertex3f(-6,0,0);
        glVertex3f(-2,2,0);
        glVertex3f(4,-3,0);
        glVertex3f(8,0,0);
        glVertex3f(10,-1,0);
        glVertex3f(10,-8,0);
    glEnd();

    glColor3f(0.2,0.2,0.2);
    retangulo(0,-4.5,0,3,20);

    glColor3f(1,1,1);
    glLineWidth(4);
    glBegin(GL_LINES);
        glVertex3f(-10,-4.5,0);
        glVertex3f(10,-4.5,0);
    glEnd();
}

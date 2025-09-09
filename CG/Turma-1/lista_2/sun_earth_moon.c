#include <stdio.h>
#include <math.h>
#include <GL/glut.h>


float w_lua = (2*3.1415)/460;
float w_terra = (2*3.1415)/6000;
int frameCounter = 0;

void display();
void animation_clock(int frame);

void sol();
void lua();
void terra();

void circulo(GLint raio, GLint n);


int main(int argc, char** argv) {
    glutInit(&argc, argv);

    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB);
    glutInitWindowSize(800, 800);
    glutInitWindowPosition(100, 100);

    glutCreateWindow("Lista 2 - Sol_Lua_Terra");
    
    // Estado Inicial
    glClearColor(0.0, 0.0, 0.0, 1.0);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(-2,2,-2,2);

    // Define callback pro display
    glutDisplayFunc(display);
    
    // Inicia o Relogio
    animation_clock(frameCounter);

    glutMainLoop();

    return 0;
}


void display() {
    glClear(GL_COLOR_BUFFER_BIT);

    glPushMatrix();
        glTranslatef(1.5*cos(w_terra*frameCounter),1.5*sin(w_terra*frameCounter),0);
        glScalef(0.6,0.6,1);
        
        glPushMatrix();
            glTranslatef(0.5*cos(w_lua*frameCounter),0.5*sin(w_lua*frameCounter),0);
            // escala
            lua();
        glPopMatrix();

        terra();
    glPopMatrix();

    sol();

    glFlush();
    glutSwapBuffers();
}

void animation_clock(int frame) {
    frameCounter = frame;
    
    glutPostRedisplay();
    glutTimerFunc(10, animation_clock, frame + 1);
}


void sol() {
    glColor3f(1,1,0.5);

    glPushMatrix();
        glScalef(0.4,0.4,1);
        circulo(1,50);
    glPopMatrix();
}

void lua() {
    glColor3f(0.855,0.882,0.906);

    glPushMatrix();
        glScalef(0.1,0.1,1);
        circulo(1,50);
    glPopMatrix();
}

void terra() {
    glColor3f(0,0,1);

    glPushMatrix();
        glScalef(0.2,0.2,1);
        circulo(1,50);
    glPopMatrix();
}

void circulo(GLint raio, GLint n) {
    glBegin(GL_POLYGON);
        for (int i=0; i<n; i++) {glVertex3f(sin((2*3.1415/n)*i),cos((2*3.1415/n)*i),0);}
    glEnd();
}

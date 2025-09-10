#include <iostream>
#include <math.h>
#include <GL/glut.h>

using namespace std;


int frameCounter = 0;

void display();
void animation_clock(int frame);

void printMtx(const GLfloat mtx[16]);


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

    GLfloat matrix[16];

    glPushMatrix();
        glTranslatef(0.5, 0.5, 0); // Matriz T1
        glRectf(-0.25, -0.25, 0.25, 0.25);

        glGetFloatv(GL_PROJECTION_MATRIX, matrix);
        printMtx(matrix);
    glPopMatrix();
        glColor3f(0.0, 0.0, 1.0);
        glPushMatrix();
        glTranslatef(0.5, 0.5, 0); // Matriz T2
        glRotatef(45.0, 0, 0, 1); // Matriz R
        glRectf(-0.25, -0.25, 0.25, 0.25);

        glGetFloatv(GL_PROJECTION_MATRIX, matrix);
        printMtx(matrix);
    glPopMatrix();

    glFlush();
    glutSwapBuffers();
}

void animation_clock(int frame) {
    frameCounter = frame;
    
    glutPostRedisplay();
    glutTimerFunc(10, animation_clock, frame + 1);
}

void printMtx(const GLfloat mtx[16]) {
    for (int i=0; i<4; i++){
        for (int j=0; j<0; j++){
            cout << mtx[j*4 + i] << '\t';
        }
        cout << endl;
    }
}

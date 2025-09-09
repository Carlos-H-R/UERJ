#include <GL/glut.h>

void display();
void reshape(GLint, GLint);
void mouse(GLint, GLint, GLint, GLint );
void square(GLfloat, GLfloat, GLfloat);




int main(int argc, char** argv){
    glutInit(&argc,argv);
    glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB);

    glutInitWindowSize (800, 800);
    glutInitWindowPosition (200, 200);

    glutCreateWindow ("Tarefa 1 - Parte 2");

    // Estado inicial
    glClearColor(1.0,1.0,1.0,1.0);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(0,800,800,0,-1,1);

    // draw
    display();
    glutReshapeFunc(reshape);
    glutMouseFunc(mouse);

    glutMainLoop();

    return 0;
}


void display(){
    glClear(GL_COLOR_BUFFER_BIT);

    glFlush();
}


void reshape(GLint width, GLint height){
    if (width == 0) 
}


void mouse(GLint button, GLint action, GLint x, GLint y){
    if (button == GLUT_LEFT_BUTTON){
        // glClear(GL_COLOR_BUFFER_BIT);
        square(x,y,0);
        glFlush();
    }

    else{
        display();
    }
}


void square(GLfloat x, GLfloat y, GLfloat z){
    glPointSize(50);
    glBegin(GL_POINTS);
        glColor3f(0.0,0.0,0.0);
        glVertex3f(x,y,z);
    glEnd();
}

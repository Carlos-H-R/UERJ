#include <GL/glut.h>


void quadrado(GLfloat x, GLfloat y, GLfloat z, GLfloat size);
void retangulo(GLfloat x, GLfloat y, GLfloat z, GLfloat height, GLfloat width);
void triangle(GLfloat x, GLfloat y, GLfloat z, GLfloat height, GLfloat base);


void display(){
    glClear(GL_COLOR_BUFFER_BIT);

    quadrado(0,0,0,0.4);
    triangle(0,0.2,0,0.2,0.5);
    retangulo(0.0,-0.1,1,0.2,0.09);

    glFlush();
}


void keyboard(unsigned char key, GLint x, GLint y){
    if (key == ' '){
        glClearColor(0.0,0.0,0.0,1.0);
    }
    
    else{
        glClearColor(1.0,1.0,1.0,1.0);
    }

    display();
}

int main(int argc, char** argv){
    glutInit(&argc,argv);
    glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB);

    glutInitWindowSize (800, 800);
    glutInitWindowPosition (200, 200);

    glutCreateWindow ("Tarefa 1 - Parte 1");

    // Estado Inicial
    glClearColor(1.0,1.0,1.0,1.0);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(-1,1,-1,1,-1,1);

    // desenho
    display();
    glutKeyboardFunc(keyboard);

    glutMainLoop();

    return 0;
}


void quadrado(GLfloat x, GLfloat y, GLfloat z, GLfloat size){
    float s = size/2;
    
    glBegin(GL_QUADS);
        glColor3f(0.0,0.0,1.0);
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
        glColor3f(0.0,1.0,0.0);
        glVertex3f(x-w,y+h,z);
        glVertex3f(x+w,y+h,z);
        glVertex3f(x+w,y-h,z);
        glVertex3f(x-w,y-h,z);
    glEnd();
}


void triangle(GLfloat x, GLfloat y, GLfloat z, GLfloat height, GLfloat base){
    float b = base/2;

    glBegin(GL_TRIANGLES);
        glColor3f(1.0,0.0,0.0);
        glVertex3f(x-b,y,z);
        glVertex3f(x,y+height,z);
        glVertex3f(x+b,y,z);
    glEnd();
}
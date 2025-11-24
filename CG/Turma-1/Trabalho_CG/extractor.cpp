#include <iostream>
#include <fstream>
#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/glut.h>

using namespace std;

std::ifstream file("./.src/dragon.obj");
// std::ifstream file("./.src/dragon.obj");
// std::ifstream file("./.src/dragon.obj");

int start_x = 0;
int start_y = 0;
int finish_x = 0;
int finish_y = 0;

GLint rot_x = 0;
GLint rot_y = 0;

void init();
void mouse(int button, int state, int x, int y);
void display();

void render();


int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH);
    glutInitWindowSize(800,800);
    glutInitWindowPosition(100,100);

    glutCreateWindow("Renderizador...");

    // Funcoes de estado do OpenGL
    glutDisplayFunc(display);
    glutMouseFunc(mouse);

    // Estado Inicial
    init();
    
    glutMainLoop();

    return 0;
}


void display() {
    // um desenhar um cubo de teste
    glBegin(GL_POLYGON);
        glVertex2d(-1.0, -1.0);
        glVertex2d(1.0, -1.0);
        glVertex2d(1.0, 1.0);
        glVertex2d(-1.0, 1.0);
    glEnd();

    glFlush();
    glutSwapBuffers();
}

void init() {
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();

    //glOrtho(-2.5, 2.5, -2.5, 2.5, 0, 2.5);
    //glOrtho(-5.0,5.0,5.0,5.0,0.0,7.5);
    gluPerspective(60,8/6,0.1,20);




    GLfloat black[] = { 0.0, 0.0, 0.0, 1.0 };
    GLfloat pink[] = { 1.0, 0.5, 1.0, 1.0 };
    GLfloat pink2[] = { 0.5, 1.0, 0.5, 1.0 };
    GLfloat yellow[] = { 1.0, 1.0, 0.0, 1.0 };
    GLfloat cyan[] = { 0.0, 1.0, 1.0, 1.0 };
    GLfloat white[] = { 1.0, 1.0, 1.0, 1.0 };
    GLfloat direction[] = { 0.0, 0.0, 10.0, 1.0 };
    GLfloat direction1[] = { 0.0,0.0, 10.0, 1.0 };

    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, cyan);
    glMaterialfv(GL_FRONT, GL_SPECULAR, white);
    glMaterialf(GL_FRONT, GL_SHININESS, 30);

    glLightfv(GL_LIGHT0, GL_AMBIENT, black);
    glLightfv(GL_LIGHT0, GL_DIFFUSE, yellow);
    glLightfv(GL_LIGHT0, GL_SPECULAR, white);
    glLightfv(GL_LIGHT0, GL_POSITION, direction);

    glLightfv(GL_LIGHT1, GL_AMBIENT, black);
    glLightfv(GL_LIGHT1, GL_DIFFUSE, white);
    glLightfv(GL_LIGHT1, GL_SPECULAR, white);
    glLightfv(GL_LIGHT1, GL_POSITION, direction1);

    glLightfv(GL_LIGHT2, GL_AMBIENT, black);
    glLightfv(GL_LIGHT2, GL_DIFFUSE, pink);
    glLightfv(GL_LIGHT2, GL_SPECULAR, white);
    glLightfv(GL_LIGHT2, GL_POSITION, direction1);

    glLightfv(GL_LIGHT3, GL_AMBIENT, black);
    glLightfv(GL_LIGHT3, GL_DIFFUSE, pink2);
    glLightfv(GL_LIGHT3, GL_SPECULAR, white);
    glLightfv(GL_LIGHT3, GL_POSITION, direction1);

    glEnable(GL_LIGHTING);
    glEnable(GL_DEPTH_TEST);
}

void mouse(int button, int state, int x, int y) {
    // atualiza a orientação do objeto baseado nos movimentos de mouse

    if ((button == GLUT_LEFT_BUTTON) && (state == GLUT_DOWN)) {
        start_x = x;
        start_y = y;
    }

    else if ((button == GLUT_LEFT_BUTTON) && (state == GLUT_UP)) {
        finish_x = x;
        finish_y = y;



        glutPostRedisplay();
    }
}

void render() {
    // le o arquivo obj e extrai o objeto a partir das informações de vetores, faces e normais
    std::string line;

    if (file.is_open()) {
        glBegin(GL_POLYGON);
        while (getline(file, line)) {
            std::istringstream iss(line); 

            char id;
            float x, y, z;
            iss >> id >> x >> y >> z; // Extract 'v' and coordinates
            std::cout << "Vertex: " << x << ", " << y << ", " << z << std::endl;
            glVertex3f(x, y, z)
        }
        glEnd();

    }


}
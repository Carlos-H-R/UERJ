#include <iostream>
#include <GL/glu.h>
#include <GL/glut.h>

using namespace std;

void rubick();

void display();
void reshape(int width, int height);
void keyboard();

int main(int argc, char** argv) {
  glutInit(&argc,argv);
  glutInitDisplayMode();

  glutInitWindowSize();
  glutInitWindowPosition();

  glutCreateWindow("Virtual Rubick");

  glclearcolor(1.0,1.)

  return 0;
}

// Desenha um cubo padrao com as cores do cubo magico
void rubick(){

}

// Desenha os objetos nos estado atual
void display() {

}

// Reconfigura a janela ao ser redimencionada
void reshape(int w, int h) {
  glViewport(0,0,(GLsizei) w,(GLsizei) h);
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  gluPerspective(85, (GLfloat) w/ (GLfloat) h, 0.1, 20.0);
  glMatrixMode(GL_MODELVIEW);
  gluLookAt(0,0,0,0,0,0,0,1,0);
}

// Processa input recebido do teclado
void keyboard(unsigned char key, int x, int y) {
  switch (key) {
  case 'a':
    /* code */
    break;
  
  default:
    break;
  }
}

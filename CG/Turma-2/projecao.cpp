#include <GL/glut.h>


void display() {
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();

  gluLookAt(0,0,10,0,0,0,0,1,0);

  glEnable(GL_LIGHT0);

  glPushMatrix();
  glTranslatef(1, 0.0, -3.0);
  glutSolidSphere(0.5, 30, 30);
  glPopMatrix();

  glDisable(GL_LIGHT0);
  glEnable(GL_LIGHT1);

  glPushMatrix();
  glTranslatef(-1, 0.0, 0.0);
  glutSolidSphere(0.5, 30, 30);
  glPopMatrix();

  glDisable(GL_LIGHT1);
  glEnable(GL_LIGHT2);

  glPushMatrix();
  glTranslatef(0.0, 1.0, -5.5);
  glutSolidSphere(0.5, 30, 30);
  glPopMatrix();

  glDisable(GL_LIGHT2);
  glEnable(GL_LIGHT3);

  glPushMatrix();
  glTranslatef(0.0, -1.0, 6);
  glutSolidSphere(0.5, 30, 30);
  glPopMatrix();

  glDisable(GL_LIGHT3);



  glFlush();
}





void init() {

  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();

  //glOrtho(-2.5, 2.5, -2.5, 2.5, 0, 2.5);
  //glOrtho(-5.0,5.0,5.0,5.0,0.0,7.5);
  gluPerspective(60,1,0.1,20);




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


int main(int argc, char** argv) {
  glutInit(&argc, argv);
  glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH);
  glutInitWindowPosition(0, 0);
  glutInitWindowSize(600, 600);
  glutCreateWindow("");
  glutDisplayFunc(display);
  init();
  glutMainLoop();
}

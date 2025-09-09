#include <GL/glut.h>


void mesa();
void cadeira();
void base();
void cross();

void display() {
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();

  gluLookAt(-5,6,8,0,0,0,0,1,0);

  glEnable(GL_LIGHT0);

	glPushMatrix();
		glScalef(2,2.5,2);
  	mesa();
	glPopMatrix();

	glPushMatrix();
		glTranslatef(-2,-1,-1.5);
		glScalef(2,2,2);
		cadeira();
	glPopMatrix();

	glPushMatrix();
		glTranslatef(2,-1,-1.5);
		glScalef(2,2,2);
		cadeira();
	glPopMatrix();

	glPushMatrix();
		glTranslatef(-2,-1,1.5);
		glRotatef(180,0,1,0);
		glScalef(2,2,2);
		cadeira();
	glPopMatrix();

	glPushMatrix();
		glTranslatef(2,-1,1.5);
		glRotatef(180,0,1,0);
		glScalef(2,2,2);
		cadeira();
	glPopMatrix();


  glFlush();
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


int main(int argc, char** argv) {
  glutInit(&argc, argv);
  glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH);
  glutInitWindowPosition(0, 0);
  glutInitWindowSize(800, 600);
  glutCreateWindow("");
  glutDisplayFunc(display);
  init();
  glutMainLoop();
}


// objetos
void mesa() {
	glColor3f(92,64,51);
  glPushMatrix();
		glTranslatef(0,1.1,0);
		glScalef(5,0.1,2.2);
		glutSolidCube(1);
	glPopMatrix();

  glPushMatrix();
		glTranslatef(-1.9,0.5,-0.9);
		glScalef(0.1,1.1,0.1);
    glRotated(45,0,1,0);
		glutSolidCube(1);
	glPopMatrix();

  glPushMatrix();
		glTranslatef(-1.9,0.5,0.9);
		glScalef(0.1,1.1,0.1);
    glRotated(45,0,1,0);
		glutSolidCube(1);
	glPopMatrix();

  glPushMatrix();
		glTranslatef(1.9,0.5,-0.9);
		glScalef(0.1,1.1,0.1);
    glRotated(45,0,1,0);
		glutSolidCube(1);
	glPopMatrix();

  glPushMatrix();
		glTranslatef(1.9,0.5,0.9);
		glScalef(0.1,1.1,0.1);
    glRotated(45,0,1,0);
		glutSolidCube(1);
	glPopMatrix();
}

void cross() {
	glPushMatrix();
		glRotated(45,0,0,1);
		glScalef(0.08,1.05,0.08);
		glutSolidCube(1);
	glPopMatrix();
	glPushMatrix();
		glRotated(-45,0,0,1);
		glScalef(0.08,1.05,0.08);
		glutSolidCube(1);
	glPopMatrix();
}
 
void base() {
	glPushMatrix();
		glTranslatef(0,1,-0.4);
		cross();
	glPopMatrix();

	glPushMatrix();
		glTranslatef(0,1,0.4);
		cross();
	glPopMatrix();

	glPushMatrix();
		glTranslatef(-0.4,1,0);
		glRotatef(90,0,1,0);
		cross();
	glPopMatrix();

	glPushMatrix();
		glTranslatef(0.4,1,0);
		glRotatef(90,0,1,0);
		cross();
	glPopMatrix();

	glPushMatrix();
		glTranslatef(0.4,1,0.4);
		glScalef(0.1,1,0.1);
  	glutSolidCube(1);
  glPopMatrix();
	 
	glPushMatrix();
		glTranslatef(0.4,1,-0.4);
		glScalef(0.1,1,0.1);
  	glutSolidCube(1);
  glPopMatrix();
	 
	glPushMatrix();
		glTranslatef(-0.4,1,0.4);
		glScalef(0.1,1,0.1);
  	glutSolidCube(1);
  glPopMatrix();
	 
	glPushMatrix();
		glTranslatef(-0.4,1,-0.4);
		glScalef(0.1,1,0.1);
  	glutSolidCube(1);
  glPopMatrix();
	 
}

void cadeira() {
	glColor3f(92,64,51);
  base();
		
	glColor3f(50,205,50);
  glPushMatrix();
		glTranslatef(0,1.45,0);
		glScalef(1.1,0.15,1.1);
		glutSolidCube(1);
	glPopMatrix();
		
  glPushMatrix();
		glTranslatef(0,2,-0.5);
		glRotatef(90,1,0,0);
		glScalef(1.1,0.15,1.1);
		glutSolidCube(1);
	glPopMatrix();
}
#include <GL/glut.h>


GLint width  = 800;
GLint height = 600;


void display();
void init();
void reshape(GLint , GLint);

void scene();
void mesa();


int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH);

    glutInitWindowPosition(50,50);
    glutInitWindowSize(width, height);

    glutCreateWindow("Tarefa 3");
	init();

    glutReshapeFunc(reshape);
    glutDisplayFunc(display);

    glutMainLoop();
}


void display() {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    glMatrixMode(GL_MODELVIEW);
    

    // x axis 2q
    glPushMatrix();
    gluLookAt(-17,4.5,0,0,4.5,0,0,1,0);
    glViewport(0,height/2,width/2,height/2);
    scene();
    glPopMatrix();

    // y axis 1q
    glPushMatrix();
    gluLookAt(0,15,2,0,0,0,0,0,-1);
    glViewport(width/2,height/2,width/2,height/2);
    scene();
    glPopMatrix();

    // z axis 3q
    glPushMatrix();
    gluLookAt(0,3,15,0,3,0,0,1,0);
    glViewport(0,0,width/2,height/2);
    scene();
    glPopMatrix();

    // diagonal 4q
    glPushMatrix();
    gluLookAt(-11,12,15,0,0,0,0,1,0);
    glViewport(width/2,0,width/2,height/2);
    scene();
    glPopMatrix();

	glFlush();
}


void init() {
    GLfloat black[] = { 0.0, 0.0, 0.0, 1.0 };
    GLfloat yellow[] = { 1.0, 1.0, 0.0, 1.0 };
    GLfloat cyan[] = { 0.0, 1.0, 1.0, 1.0 };
    GLfloat brown[] = { 0.588, 0.435, 0.2, 1.0};
    GLfloat white[] = { 1.0, 1.0, 1.0, 1.0 };
    GLfloat direction[] = { 0.0, -10.0, 0.0, 1.0 };
    GLfloat direction1[] = { 0.0, 10.0, 0.0, 1.0 };

    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, cyan);
    glMaterialfv(GL_FRONT, GL_SPECULAR, white);
    glMaterialf (GL_FRONT, GL_SHININESS, 60);

    glLightfv(GL_LIGHT0, GL_AMBIENT, black);
    glLightfv(GL_LIGHT0, GL_DIFFUSE, white);
    glLightfv(GL_LIGHT0, GL_SPECULAR, white);
    glLightfv(GL_LIGHT0, GL_POSITION, direction);

    glLightfv(GL_LIGHT1, GL_AMBIENT, black);
    glLightfv(GL_LIGHT1, GL_DIFFUSE, white);
    glLightfv(GL_LIGHT1, GL_SPECULAR, white);
    glLightfv(GL_LIGHT1, GL_POSITION, direction1);

    glEnable(GL_LIGHTING);
    glEnable(GL_LIGHT0);
	glEnable(GL_LIGHT1);
    glEnable(GL_DEPTH_TEST);
}


void scene() {
    glPushMatrix();
	glScalef(5,5,5);
    mesa();
	glPopMatrix();

	glPushMatrix();
	glTranslatef(0,8.9,0);
	glScalef(3,3,3);
	glutSolidSphere(1,30,30);
	glPopMatrix();
}


void reshape(GLint w, GLint h) {
    width = w; height = h;

    glMatrixMode(GL_PROJECTION);
    GLfloat aspect = GLfloat(w) / GLfloat(h);
    glLoadIdentity();

    gluPerspective(110,aspect,0.1,50);
}


// objetos
void mesa() {
    glPushMatrix();
	glTranslatef(0,1.1,0);
	glScalef(5,0.2,2.2);
	glutSolidCube(1);
	glPopMatrix();

    glPushMatrix();
	glTranslatef(-1.9,0.5,-0.9);
	glScalef(0.1,1,0.1);
    glRotated(45,0,1,0);
	glutSolidCube(1);
	glPopMatrix();

    glPushMatrix();
	glTranslatef(-1.9,0.5,0.9);
	glScalef(0.1,1,0.1);
    glRotated(45,0,1,0);
	glutSolidCube(1);
	glPopMatrix();

    glPushMatrix();
	glTranslatef(1.9,0.5,-0.9);
	glScalef(0.1,1,0.1);
    glRotated(45,0,1,0);
	glutSolidCube(1);
	glPopMatrix();

    glPushMatrix();
	glTranslatef(1.9,0.5,0.9);
	glScalef(0.1,1,0.1);
    glRotated(45,0,1,0);
	glutSolidCube(1);
	glPopMatrix();
}


//primitivas esfera, cubo, torus (acho q tem na glut)
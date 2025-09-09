#include <GL/glut.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>

#define RAND_MAX = 30


typedef struct Position {
	GLfloat x;
	GLfloat y;
	GLfloat z;
}Position;


Position astro;
Position playerP;
Position itemPosition;

GLfloat center;
GLfloat health;
GLfloat speed;
GLfloat move;

GLint frames;
GLint itemType;

GLboolean isDay;
GLboolean vehicleOn;
GLboolean itemCaptured;
GLboolean colision;


void init();
void frameConter(GLint);
void display();
void reshape(GLint, GLint);
void keyboard(unsigned char, GLint, GLint);

void sky();
void background();

void sun();
void moon(GLint);
void cloud(GLint);

void playerInterface();
void character();
void vehicle();

void missile();
void plane();

void itemController();
void spaceBox();    // summon vehicle
void heart();       // recover health
void energyCore();  // increase speed for a while

void triangle(GLfloat);
void quad(GLfloat, GLfloat);
void circle(GLint);
void circle_edge(GLint);

void astroPath();


int main(int argc, char** argv) {
	srand(time(NULL));
	
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB);


	glutInitWindowSize(800,800);
	glutInitWindowPosition(50,50);

	glutCreateWindow("Trabalho 1");
	init();

	glutDisplayFunc(display);
	glutKeyboardFunc(keyboard);

	glutMainLoop();

	return 0;
}


void init() {
	center = 2;

	itemType = rand() % 3;
	itemPosition.z = 0;
	itemPosition.x = rand() % 40;
	itemPosition.y = -6.5;
	
	frames = 0;
	frameConter(frames);

	move = 0; 
	playerP.x = 0;
	playerP.y = 0;
	playerP.z = 0;
	speed = 3;
	health = 100;

	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	glOrtho(-10,10,-10,10,1,-1);
}

void frameConter(GLint frame) {
	GLfloat dist = abs(itemPosition.x);
	if (dist <= 0.1) colision = true;


	frames ++;
	glutPostRedisplay();

	glutTimerFunc(10,frameConter,frame);
}

void display() {
	glMatrixMode(GL_MODELVIEW);

	if (isDay)	glClearColor(0.5294,0.8078,0.9216,1);
	else glClearColor(0.0468,0.0781,0.2695,1);

	glClear(GL_COLOR_BUFFER_BIT);

	sky();
	background();
	playerInterface();
	itemController();

	glFlush();
	glutSwapBuffers();
}

void reshape(GLint width, GLint height) {
	// based on width and height 
	// reconfigure exibition of the window
}

void keyboard(unsigned char key, GLint x, GLint y) {
	switch (key)
	{
	case 'a':
		itemPosition.x += 0.05 * speed;
		move -= 1;
		center -= 0.05 * speed;
		if (center < 0) center = 80;
		glutPostRedisplay();
		break;
	
	case 'A':
		itemPosition.x += 0.05 * speed;
		move -= 2;
		center -= 0.1 * speed;
		if (center < 0) center = 80;
		glutPostRedisplay();
		break;
	
	case 'd':
		itemPosition.x -= 0.05 * speed;
		move += 1;
		center += 0.05 * speed;
		if (center >= 80) {
			center = 0;
			itemCaptured = false;
			itemType = rand() % 3;
		}
		glutPostRedisplay();
		break;
	
	case 'D':
		itemPosition.x -= 0.05 * speed;
		move += 2;
		center += 0.1 * speed;
		if (center >= 80) {
			center = 0;
			itemCaptured = false;
			itemType = rand() % 3;
		}
		glutPostRedisplay();
		break;
	
	// case 'w':
	// 	playerP.y += 0.1;
	// 	center += 0.1;
	// 	if (center >= 80) center = 0;
	// 	glutPostRedisplay();
	// 	break;
	
	default:
		break;
	}
}


// elementos interativos do jogo


void sky() {
	isDay = (frames % 10000) < 5000;
	astroPath();

	glPushMatrix();
		glTranslatef(astro.x,astro.y,astro.z);
        if (isDay) sun();
        else moon(5);
	glPopMatrix();
}

void background() { // subdivide into land, sky and front elements
	// control the background color (day and night cycle based on time)

	glColor3f(0.457,0.6133,0.7421);
	glPushMatrix();
		glTranslatef(-0.25*center,0,0);
		glPushMatrix();
			glTranslatef(-6,-1,0);
			glScalef(10,13,0);
			triangle(1);
		glPopMatrix();
		
		glPushMatrix();
			glTranslatef(0,-1,0);
			glScalef(11,13,0);
			triangle(1);
		glPopMatrix();
		
		glPushMatrix();
			glTranslatef(6,-1,0);
			glScalef(11,15,0);
			triangle(1);
		glPopMatrix();
			
		glPushMatrix();
			glTranslatef(14,-1,0);
			glScalef(10,13,0);
			triangle(1);
		glPopMatrix();
		
		glPushMatrix();
			glTranslatef(20,-1,0);
			glScalef(11,13,0);
			triangle(1);
		glPopMatrix();
		
		glPushMatrix();
			glTranslatef(26,-1,0);
			glScalef(11,15,0);
			triangle(1);
		glPopMatrix();
	glPopMatrix();
	
	glColor3f(0.4863,0.9882,0.0);
	glPushMatrix();
		glTranslatef(-0.5*center,0,0);
		glBegin(GL_POLYGON);
			glVertex3f(-10,-10,0);
			glVertex3f(-10,0,0);
			glVertex3f(10,1,0);
			glVertex3f(20,0.2,0);
			glVertex3f(30,0,0);
			glVertex3f(50,1,0);
			glVertex3f(50,-10,0);
		glEnd();
		// put the background elements here so they enter the loop (between -10 and 50)
		glColor3f(0.07,0.04,0.02);
		glPushMatrix();
			glTranslatef(20,-6.5,0);
			quad(60,3.5);
			glColor3f(1,1,1);
			quad(60,0.1);
		glPopMatrix();
	glPopMatrix();

	int cloudCycle = frames % 8000;
	// clouds (need to include clouds loop)
	glPushMatrix();
		glTranslatef(-26+(cloudCycle*0.005),8,1);
		glScalef(1.3,1.3,1);
        cloud(0);
	glPopMatrix();
	glPushMatrix();
		glTranslatef(-12+(cloudCycle*0.005),7,1);
		cloud(0);
	glPopMatrix();
	
}


// objetos compostos
void sun() {
	glColor4f(0.9922,0.9843,0.8275,1);
	circle(30);
	glColor3f(1,1,0);
	circle_edge(30);
}

void moon(GLint phase) {
    switch (phase)
    {
    case 5:
	    glColor4f(0.9609,0.9414,0.832,0.5);
	    circle(30);
	    glColor4f(0.9609,0.9414,0.9025,0.5);
			circle_edge(30);
      break;
    
    default:
	    glColor4f(0.9609,0.9414,0.832,0.5);
	    circle(30);
      break;
    }
}

void cloud(GLint type) {
	glColor3f(0.921,0.901,0.847);

	switch (type)
	{
	case 0:
		quad(1.5,0.5);
		glPushMatrix();
			glTranslatef(-0.75,0,0);
			glScalef(0.25,0.25,1);
			circle(30);
		glPopMatrix();
		glPushMatrix();
			glTranslatef(0.75,0,0);
			glScalef(0.25,0.25,1);
			circle(30);
		glPopMatrix();
		glPushMatrix();
			glTranslatef(-0.25,0.25,0);
			glScalef(0.5,0.5,1);
			circle(30);
		glPopMatrix();
		glPushMatrix();
			glTranslatef(0.2,0.3,0);
			glScalef(0.5,0.3,1);
			circle(30);
		glPopMatrix();
		break;
	
	default:
		circle(30);
		break;
	}
}


// Game Objects
void playerInterface() {
	// control if is the vehicle or alien
	// control movements

	if (vehicleOn) {
		glPushMatrix();
			glTranslatef(0,-5,0);
			vehicle();
		glPopMatrix();
	}

	else {
		glPushMatrix();
			glTranslatef(0,-6.5,0);
			character();
		glPopMatrix();
	}
}

void character() {
	glColor3f(0.5,0.5,0.5);
	quad(0.1,0.3);
	glPushMatrix();
		glTranslatef(0,-0.2,0);
		quad(0.1,0.25);
	glPopMatrix();
	glPushMatrix();
		glTranslatef(0,-0.4,0);
		glRotatef(-move*2,0,0,1);
		quad(0.05,0.5);
	glPopMatrix();
	glPushMatrix();
		glTranslatef(0,0.25,0);
		glScalef(0.2,0.2,1);
		circle(30);
	glPopMatrix();
}

void vehicle() {
	glColor3f(0.67,0.67,0.67);
	glPushMatrix();
		glScalef(1.5,0.6,1);
		circle(30);
	glPopMatrix();

	glColor3f(0.7773,0.8867,0.8789);
	glPushMatrix();
		glTranslatef(0,0.5,0);
		glScalef(0.5,0.5,0);
		circle(30);
	glPopMatrix();
}


// Interactive Objects
void itemController() {
	if (!itemCaptured) {
		itemCaptured = colision;
		switch (itemType)
		{
		case 0:
			glPushMatrix();
				glTranslatef(itemPosition.x,itemPosition.y,itemPosition.z);
				heart();
			glPopMatrix();

			if (colision) health += 20;
			break;

		case 1:
			glPushMatrix();
				glTranslatef(itemPosition.x,itemPosition.y,itemPosition.z);
				energyCore();
			glPopMatrix();

			if (colision) speed += 0.1;
			break;

		case 2:
			glPushMatrix();
				glTranslatef(itemPosition.x,itemPosition.y,itemPosition.z);
				spaceBox();
			glPopMatrix();

			if (colision) vehicleOn = true;
			break;

		default:
			break;
		}
	}
}	

void spaceBox() {
	glPushMatrix();
		glRotatef(1,0,0,1);
		glColor3f(0.33,0.33,0.33);

		quad(0.5,0.5);

		glColor3f(0.3125,0.7812,0.4687);
		glPushMatrix();
			glScalef(0.1,0.1,1);
			circle(30);
		glPopMatrix();
}

void heart() {
	glColor3f(1,0,0);

	glPushMatrix();
		glRotatef(60,0,0,1);
		triangle(0.33);
	glPopMatrix();

	glPushMatrix();
		glTranslatef(-0.075,0.07,0);
		glScalef(0.075,0.075,1);
		circle(30);
	glPopMatrix();

	glPushMatrix();
		glTranslatef(0.075,0.07,0);
		glScalef(0.075,0.075,1);
		circle(30);
	glPopMatrix();
}

void energyCore() {
	glPushMatrix();
		glScalef(0.25,0.25,1);
		glColor3f(1,1,0);
		circle(30);
		glColor3f(0,0,0);
		circle_edge(30);
	glPopMatrix();

	glColor3f(0.3125,0.7812,0.4687);
	glPushMatrix();
		glRotatef(45,0,0,1);
		quad(0.2,0.2);
	glPopMatrix();
	quad(0.2,0.2);
}


// Primitivas
void triangle(GLfloat side) {
	GLfloat h = (side * sqrt(3)) / 2;
	GLfloat x = side / 2;

	glBegin(GL_TRIANGLES);
		glVertex3f( 0,(2*h)/3, 0);
		glVertex3f( x,-(h/3), 0);
		glVertex3f(-x,-(h/3), 0);
	glEnd();
}

void quad(GLfloat width, GLfloat height) {
	GLfloat w = width / 2;
	GLfloat h = height / 2;

	glBegin(GL_QUADS);
		glVertex3f( w, h, 0);
		glVertex3f( w,-h, 0);
		glVertex3f(-w,-h, 0);
		glVertex3f(-w, h, 0);
	glEnd();
}

void circle(GLint n) {
    glBegin(GL_POLYGON);
        for (int i=0; i<n; i++) {glVertex3f(sin((2*M_PI/n)*i),cos((2*M_PI/n)*i),0);}
    glEnd();
}


void circle_edge(GLint n) {
    glBegin(GL_LINE_LOOP);
        for (int i=0; i<n; i++) {glVertex3f(sin((2*M_PI/n)*i),cos((2*M_PI/n)*i),0);}
    glEnd();
}


void astroPath() {
	GLfloat time = frames % 5000;
	GLfloat fTime = time / 5000;

	// astro.z = 0;
	// astro.x = 0;
	// astro.y = 8.5;

	astro.x = -12 + (24*fTime);
	astro.z =  0;
	astro.y =  8.5 + (-0.1 * pow(astro.x,2));
}


/* 
1000 frames pra deslizar a cor de azul ceu pra alaranjado (4000 -> 5000)
1000 frames pra deslizar do alaranjado para as cores noturnas (0 -> 1000)
*/

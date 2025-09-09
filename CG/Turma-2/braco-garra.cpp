#ifdef __APPLE_CC__
#include <GLUT/glut.h>
#else
#include <GL/glut.h>
#endif

static int shoulder = 0, elbow = 0, index = 0, middle = 0, pol = 0;

void init(void){
  // glClearColor (0.0, 0.0, 0.0, 0.0);

  glEnable(GL_DEPTH_TEST);
  glEnable(GL_CULL_FACE);
}

void display(void){
  glClear (GL_COLOR_BUFFER_BIT);

  glPushMatrix();


  glRotatef ((GLfloat) shoulder, 0.0, 0.0, 1.0);


  glPushMatrix();
  glScalef (2.0, 0.4, 1.0);
  glColor3f(1,0,0);
  glutSolidCube (1.0);
  glColor3f(0,0,0);
  glutWireCube (1.0);
  glPopMatrix();

  glTranslatef (1.0, 0.0, 0.0);
  glRotatef ((GLfloat) elbow, 0.0, 0.0, 1.0);

  glPushMatrix();
  glTranslatef (1.0, 0.0, 0.0);
  glScalef (2.0, 0.4, 1.0);
  glColor3f(0,1,0);
  glutSolidCube (1.0);
  glColor3f(0,0,0);
  glutWireCube (1.0);
  glPopMatrix();

  //index
  glPushMatrix();
  glTranslatef(2.0,0.2,-0.4);
  glRotatef(GLfloat(index),0.0,0.0,1.0);
  glTranslatef(0.5,0.0,0.0);
  glScalef(1.0,0.2,0.2);
  glColor3f(1,0,1);
  glutSolidCube(1.0);
  glColor3f(0,0,0);
  glutWireCube(1.0);
  glPopMatrix();

  // //middle
  glPushMatrix();
  glTranslatef(2.0,0.2,0.4);
  glRotatef(GLfloat(middle),0.0,0.0,1.0);
  glTranslatef(0.5,0.0,0.0);
  glScalef(1.0,0.2,0.2);
  glColor3f(0,1,1);
  glutSolidCube(1.0);
  glColor3f(0,0,0);
  glutWireCube(1.0);
  glPopMatrix();

  // //pol
  glPushMatrix();
  glTranslatef(2.0,-0.2,0.0);
  glRotatef(GLfloat(pol),0.0,0.0,1.0);
  glTranslatef(0.4,0.0,0.0);
  glScalef(0.8,0.2,0.2);
  glColor3f(1,1,0);
  glutSolidCube(1.0);
  glColor3f(0,0,0);
  glutWireCube(1.0);
  glPopMatrix();

  glPopMatrix();
  glutSwapBuffers();
}

void reshape (int w, int h){
  glViewport (0, 0, (GLsizei) w, (GLsizei) h);
  glMatrixMode (GL_PROJECTION);
  glLoadIdentity ();
  gluPerspective(85, (GLfloat) w/(GLfloat) h, 0.1, 20.0);
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();
  gluLookAt(0,0,5,0,0,0,0,1,0);
}

void keyboard (unsigned char key, int x, int y){
  switch (key) {
  case 's':
    shoulder = (shoulder + 5) % 360;
    glutPostRedisplay();
    break;
  case 'S':
    shoulder = (shoulder - 5) % 360;
    glutPostRedisplay();
    break;
  case 'e':
    elbow = (elbow + 5) % 360;
    glutPostRedisplay();
    break;
  case 'E':
    elbow = (elbow - 5) % 360;
    glutPostRedisplay();
    break;
  case 'i':
    index = (index + 5) % 360;
    glutPostRedisplay();
    break;
  case 'I':
    index = (index - 5) % 360;
    glutPostRedisplay();
    break;
  case 'm':
    middle = (middle + 5) % 360;
    glutPostRedisplay();
    break;
  case 'M':
    middle = (middle - 5) % 360;
    glutPostRedisplay();
    break;
  case 'p':
    pol = (pol + 5) % 360;
    glutPostRedisplay();
    break;
  case 'P':
    pol = (pol - 5) % 360;
    glutPostRedisplay();
    break;
  case 27:
    exit(0);
    break;
  default:
    break;
  }
}

int main(int argc, char** argv){
  glutInit(&argc, argv);
  glutInitDisplayMode (GLUT_DOUBLE | GLUT_RGB);
  glutInitWindowSize (500, 500);
  glutInitWindowPosition (100, 100);
  glutCreateWindow (argv[0]);
  init ();
  glutDisplayFunc(display);
  glutReshapeFunc(reshape);
  glutKeyboardFunc(keyboard);
  glutMainLoop();
  return 0;
}

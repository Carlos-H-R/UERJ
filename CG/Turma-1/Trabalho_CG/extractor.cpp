#include <iostream>
#include <fstream>
#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/glut.h>

using namespace std;

// Para selecionar qual o arquivo a ser lido eh so descomentar uma das linhas abaixo
std::ifstream file("./.src/dragon.obj");
// std::ifstream file("./.src/dragon.obj");
// std::ifstream file("./.src/dragon.obj");

int start_x = 0;
int start_y = 0;
int finish_x = 0;
int finish_y = 0;

GLint rot_x = 0;
GLint rot_y = 0;

struct Vec3 {
    float x, y, z;
};

struct Vertex {
    Vec3 position;
    Vec3 normal;
};

std::vector<glm::vec3> vertices;
std::vector<glm::vec3> faces;
std::vector<glm::vec3> normal;

void init();
void mouse(int button, int state, int x, int y);
void display();

void reader();
void drawModel();


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
    reader();
    glutMainLoop();

    return 0;
}


void display() {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    // Posiciona a camera
    gluLookAt(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0);

    // Aplica as rotações
    glRotatef(rot_y, 1.0, 0.0, 0.0);
    glRotatef(rot_x, 0.0, 1.0, 0.0);


    // Desenha o modelo carregado do arquivo .obj
    drawModel();

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

void mouse(int button, int state, int x, int y) {
    // atualiza a orientação do objeto baseado nos movimentos de mouse

    if ((button == GLUT_LEFT_BUTTON) && (state == GLUT_DOWN)) {
        start_x = x;
        start_y = y;
    }

    else if ((button == GLUT_LEFT_BUTTON) && (state == GLUT_UP)) {
        finish_x = x;
        finish_y = y;

        rot_x += start_y - finish_y;
        rot_y += start_x - finish_x;

        glutPostRedisplay();
    }
}

void reader() {
    // le o arquivo obj e extrai o objeto a partir das informações de vetores, faces e normais
    std::string line;

    if (file.is_open()) {
        while (getline(file, line)) {
            std::istringstream stream(line); 
            std::string id;
            stream >> id;

            if (id == "v"){
                Vec3 vertex;
                ss >> vertex.x >> vertex.y >> vertex.z;
                vertices.push_back(vertex);
            }

            else if (id == "f") {
                unsigned int vIndex[3], nIndex[3];
                
                int matches = fscanf(file, "%d//%d %d//%d %d//%d\n", 
                                    &vIndex[0], &nIndex[0],
                                    &vIndex[1], &nIndex[1],
                                    &vIndex[2], &nIndex[2]);

                if (matches != 6) {
                    printf("Erro: Formato de face deve ser v//vn\n");
                }

                Vertex newVertex;
                
                newVertex.position.x = vIndex[0] - 1;
                newVertex.position.y = vIndex[1] - 1;
                newVertex.position.z = vIndex[2] - 1;
                newVertex.normal.x   = nIndex[0] - 1;
                newVertex.normal.y   = nIndex[1] - 1;
                newVertex.normal.z   = nIndex[2] - 1;
                faces.push_back(newVertex);
            }

            else if (id == "vn") {
                Vec3 normal;
                ss >> normal.x >> normal.y >> normal.z;
                normals.push_back(normal);
            }

        }
    }
}

void drawModel() {
    float centerX = (modelMin.x + modelMax.x) / 2.0f;
    float centerY = (modelMin.y + modelMax.y) / 2.0f;
    float centerZ = (modelMin.z + modelMax.z) / 2.0f;
    
    float sizeX = modelMax.x - modelMin.x;
    float sizeY = modelMax.y - modelMin.y;
    float sizeZ = modelMax.z - modelMin.z;
    float maxDim = std::max({sizeX, sizeY, sizeZ});

    float scale = 2.0f / maxDim;

    glPushMatrix();
    glScalef(scale, scale, scale);
    glTranslatef(-centerX, -centerY, -centerZ);

    for (const auto& face : faces) {
        if (face.position.empty()) continue; // Ignora faces vazias

        glBegin(GL_POLYGON); 
        for (size_t i = 0; i < face.position.size(); ++i) {
            size_t v_idx = face.position[i];
            
            if (i < face.normal.size() && !normal.empty()) {
                size_t n_idx = face.normal[i];
                if (n_idx > 0 && n_idx <= normal.size()) { // Ignora índice inválido
                    const Vertex& nm = normal[n_idx];
                    glNormal3f(nm.x, nm.y, nm.z);
                }
            }
            const Vertex& vertex = vertices[v_idx];
            glVertex3f(vertex.x, vertex.y, vertex.z);
        }
        glEnd();
    }
    glPopMatrix();
        
}

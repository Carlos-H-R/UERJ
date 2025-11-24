#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <limits>
#include <algorithm>
#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/glut.h>

using namespace std;

// Estruturas para armazenar os dados do modelo
struct Vertex {
    float x, y, z;
};

struct Face {
    vector<int> vertexIndices;
    vector<int> normalIndices;
};

vector<Vertex> vertices;
vector<Vertex> normals;
vector<Face> faces;
Vertex modelMin = {numeric_limits<float>::max(), numeric_limits<float>::max(), numeric_limits<float>::max()};
Vertex modelMax = {numeric_limits<float>::lowest(), numeric_limits<float>::lowest(), numeric_limits<float>::lowest()};

// Variáveis de rotação
GLfloat rot_x = 0.0f;
GLfloat rot_y = 0.0f;
int last_x = 0;
int last_y = 0;
bool is_rotating = false;

void init();
void display();
void mouse(int button, int state, int x, int y);
void motion(int x, int y);
void loadModel(const string& filename);
void drawModel();

int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH);
    glutInitWindowSize(800, 600);
    glutInitWindowPosition(100, 100);
    glutCreateWindow("Leitor de OBJ - Cumulus");

    init();
    loadModel(".src/cumulus00.obj");

    glutDisplayFunc(display);
    glutMouseFunc(mouse);
    glutMotionFunc(motion);

    glutMainLoop();

    return 0;
}

void init() {
    glClearColor(0.1f, 0.1f, 0.1f, 1.0f);
    glEnable(GL_DEPTH_TEST);
    glEnable(GL_LIGHTING);
    glEnable(GL_LIGHT0);

    GLfloat light_pos[] = {2.0, 2.0, 2.0, 1.0};
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos);

    GLfloat ambient[] = {0.2, 0.2, 0.2, 1.0};
    GLfloat diffuse[] = {0.8, 0.8, 0.8, 1.0};
    GLfloat specular[] = {1.0, 1.0, 1.0, 1.0};

    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient);
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse);
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular);

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(60.0, 800.0 / 600.0, 0.1, 100.0);
}

void loadModel(const string& filename) {
    // Clear previous model data
    vertices.clear();
    normals.clear();
    faces.clear();
    modelMin = {numeric_limits<float>::max(), numeric_limits<float>::max(), numeric_limits<float>::max()};
    modelMax = {numeric_limits<float>::lowest(), numeric_limits<float>::lowest(), numeric_limits<float>::lowest()};

    ifstream file(filename);
    if (!file.is_open()) {
        cerr << "Erro ao abrir o arquivo: " << filename << endl;
        return;
    }

    string line;
    while (getline(file, line)) {
        stringstream ss(line);
        string type;
        ss >> type;

        if (type == "v") {
            Vertex v;
            ss >> v.x >> v.y >> v.z;
            vertices.push_back(v);
            modelMin.x = min(modelMin.x, v.x);
            modelMin.y = min(modelMin.y, v.y);
            modelMin.z = min(modelMin.z, v.z);
            modelMax.x = max(modelMax.x, v.x);
            modelMax.y = max(modelMax.y, v.y);
            modelMax.z = max(modelMax.z, v.z);
        } else if (type == "vn") {
            Vertex n;
            ss >> n.x >> n.y >> n.z;
            normals.push_back(n);
        } else if (type == "f") {
            Face f;
            string vertex_str;
            while (ss >> vertex_str) {
                stringstream face_ss(vertex_str);
                string index_str;
                int v_idx = 0, vt_idx = 0, vn_idx = 0;

                getline(face_ss, index_str, '/');
                if (!index_str.empty()) v_idx = stoi(index_str);

                if (getline(face_ss, index_str, '/')) {
                    if (!index_str.empty()) vt_idx = stoi(index_str);
                }

                if (getline(face_ss, index_str, '/')) {
                    if (!index_str.empty()) vn_idx = stoi(index_str);
                }

                if (v_idx != 0) f.vertexIndices.push_back(v_idx);
                if (vn_idx != 0) f.normalIndices.push_back(vn_idx);
            }
            faces.push_back(f);
        }
    }
    cout << "Modelo carregado: " << vertices.size() << " vertices, " << faces.size() << " faces." << endl;
}

void display() {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    gluLookAt(0.0, 0.0, 5.0,
              0.0, 0.0, 0.0,
              0.0, 1.0, 0.0);

    glRotatef(rot_y, 1.0, 0.0, 0.0);
    glRotatef(rot_x, 0.0, 1.0, 0.0);

    GLfloat mat_ambient[] = { 0.7f, 0.7f, 0.7f, 1.0f };
    GLfloat mat_diffuse[] = { 0.8f, 0.8f, 0.8f, 1.0f };
    GLfloat mat_specular[] = { 1.0f, 1.0f, 1.0f, 1.0f };
    GLfloat mat_shininess[] = { 100.0f };

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient);
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse);
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular);
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess);

    drawModel();

    glFlush();
}

void drawModel() {
    if (vertices.empty()) return;

    float centerX = (modelMin.x + modelMax.x) / 2.0f;
    float centerY = (modelMin.y + modelMax.y) / 2.0f;
    float centerZ = (modelMin.z + modelMax.z) / 2.0f;
    
    float sizeX = modelMax.x - modelMin.x;
    float sizeY = modelMax.y - modelMin.y;
    float sizeZ = modelMax.z - modelMin.z;
    float maxDim = std::max({sizeX, sizeY, sizeZ});
    
    if (maxDim == 0) maxDim = 1.0;

    float scale = 2.0f / maxDim;

    glPushMatrix();
    
    glScalef(scale, scale, scale);
    glTranslatef(-centerX, -centerY, -centerZ);

    for (const auto& face : faces) {
        if (face.vertexIndices.empty()) continue;

        glBegin(GL_POLYGON);
        for (size_t i = 0; i < face.vertexIndices.size(); ++i) {
            size_t v_idx = face.vertexIndices[i];
            if (v_idx == 0 || v_idx > vertices.size()) continue;
            
            if (i < face.normalIndices.size() && !normals.empty()) {
                size_t n_idx = face.normalIndices[i];
                if (n_idx > 0 && n_idx <= normals.size()) {
                    const Vertex& normal = normals[n_idx - 1];
                    glNormal3f(normal.x, normal.y, normal.z);
                }
            }
            const Vertex& vertex = vertices[v_idx - 1];
            glVertex3f(vertex.x, vertex.y, vertex.z);
        }
        glEnd();
    }
    glPopMatrix();
}


void mouse(int button, int state, int x, int y) {
    if (button == GLUT_LEFT_BUTTON) {
        if (state == GLUT_DOWN) {
            is_rotating = true;
            last_x = x;
            last_y = y;
        } else {
            is_rotating = false;
        }
    }
}

void motion(int x, int y) {
    if (is_rotating) {
        rot_x += (x - last_x);
        rot_y += (y - last_y);
        last_x = x;
        last_y = y;
        glutPostRedisplay();
    }
}

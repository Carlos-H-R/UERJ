void display() {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    // Posiciona a camera
    gluLookAt(0.0, 0.0, 5.0,  // eye
              0.0, 0.0, 0.0,  // center
              0.0, 1.0, 0.0); // up

    // Aplica as rotações
    glRotatef(rot_y, 1.0, 0.0, 0.0);
    glRotatef(rot_x, 0.0, 1.0, 0.0);


    // Desenha o modelo carregado do arquivo .obj
    drawModel();

    glFlush();
}
void drawModel() {
    if (vertices.empty()) return;

    // Calcula o centro e a maior dimensão do modelo a partir da Bounding Box
    float centerX = (modelMin.x + modelMax.x) / 2.0f;
    float centerY = (modelMin.y + modelMax.y) / 2.0f;
    float centerZ = (modelMin.z + modelMax.z) / 2.0f;
    
    float sizeX = modelMax.x - modelMin.x;
    float sizeY = modelMax.y - modelMin.y;
    float sizeZ = modelMax.z - modelMin.z;
    float maxDim = std::max({sizeX, sizeY, sizeZ});
    
    // Evita divisão por zero se o modelo não tiver volume
    if (maxDim == 0) maxDim = 1.0;

    float scale = 2.0f / maxDim; // Calcula a escala para caber numa "caixa" de visualização de tamanho 2

    glPushMatrix();
    
    // 1. Escala para o tamanho correto
    glScalef(scale, scale, scale);
    // 2. Translada o centro do modelo para a origem (0,0,0)
    glTranslatef(-centerX, -centerY, -centerZ);

    for (const auto& face : faces) {
        if (face.vertexIndices.empty()) continue; // Ignora faces vazias

        glBegin(GL_POLYGON); // Volta a usar GL_POLYGON para faces com mais de 3 vértices
        for (size_t i = 0; i < face.vertexIndices.size(); ++i) { // Itera por todos os vértices da face
            size_t v_idx = face.vertexIndices[i];
            // Checagem de segurança do índice do vértice
            if (v_idx == 0 || v_idx > vertices.size()) continue; // Ignora índice inválido
            
            // Checagem de segurança do índice da normal
            if (i < face.normalIndices.size() && !normals.empty()) {
                size_t n_idx = face.normalIndices[i];
                if (n_idx > 0 && n_idx <= normals.size()) { // Ignora índice inválido
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
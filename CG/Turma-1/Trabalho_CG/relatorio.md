# Relatório de Atividade - Renderizador de Modelos .OBJ

<br><br><br><br><br><br><br><br><br><br>
<br><br><br><br><br><br><br><br><br><br>

---
**Nome do Aluno:** _________________________
<br>
**Matrícula:** _________________________

<div style="page-break-after: always;"></div>

## 1. Construindo e Utilizando o Programa

Esta seção detalha os passos necessários para compilar o programa em um ambiente Linux e como utilizá-lo para carregar diferentes modelos 3D.

### 1.1 Compilação do Executável

O programa foi desenvolvido em C++ e utiliza as bibliotecas OpenGL e GLUT para renderização gráfica. Para compilar o código-fonte (`extractor.cpp`) e gerar o arquivo executável, utilize o seguinte comando no terminal:

```bash
g++ extractor.cpp -o extractor -lGL -lGLU -lglut
```

Este comando irá gerar um arquivo executável chamado `extractor` no mesmo diretório.

### 1.2 Carregando Modelos

Para carregar um modelo 3D diferente, é necessário modificar o arquivo-fonte `extractor.cpp`. A chamada para o carregamento do modelo está localizada na função `init()`.

**Exemplo:**
Para carregar o modelo `teapot.obj`, a linha de código correspondente deve ser:
```cpp
loadModel("./.src/teapot.obj");
```

Para carregar o modelo `dragon.obj`, a linha deve ser:
```cpp
loadModel("./.src/dragon.obj");
```

Após modificar o arquivo, é necessário recompilar o programa seguindo o passo 1.1 para que as alterações tenham efeito. Os arquivos de modelo (`.obj`) devem estar localizados no diretório `.src/`.

## 2. Modelos Utilizados

Durante o desenvolvimento e depuração do programa, diversos modelos foram testados para garantir a funcionalidade do renderizador. O programa demonstrou sucesso ao carregar, centralizar, escalar e renderizar modelos que seguem o padrão de formato `.obj` e que possuem geometria válida.

Modelos que foram carregados com sucesso incluem:

1.  **`teapot.obj`**: O modelo clássico de bule de chá (Utah teapot), que foi renderizado corretamente após a implementação da lógica de carregamento e auto-escala.
2.  **`[Nome do Modelo 2]`**: (Espaço para descrever outro modelo testado).
3.  **`[Nome do Modelo 3]`**: (Espaço para descrever outro modelo testado).

O modelo `dragon.obj` apresentou problemas de renderização que não foram resolvidos durante os testes. A causa provável está relacionada a dados corrompidos, geometria não-padrão (polígonos complexos, não-convexos) ou outra inconsistência no próprio arquivo de dados, uma vez que o renderizador se mostrou funcional com o modelo `teapot.obj`.

## 3. Recursos Adicionais

Para a correta compilação e execução do programa, os seguintes recursos são necessários:

*   **Compilador C++:** Um compilador C++ padrão, como o `g++`.
*   **Bibliotecas Gráficas:** As bibliotecas de desenvolvimento para OpenGL e GLUT. Em sistemas baseados em Debian (como Ubuntu), elas podem ser instaladas com o seguinte comando:
    ```bash
    sudo apt-get install freeglut3-dev
    ```
    Em sistemas baseados em Arch Linux, o comando seria:
    ```bash
    sudo pacman -S freeglut
    ```
*   **Arquivos de Modelo:** Os arquivos de modelo no formato `.obj` que se deseja renderizar. Por convenção do projeto, estes devem ser colocados no diretório `./.src/`.

## 4. Informações Adicionais

*   **Processo de Depuração:** O desenvolvimento foi iterativo, partindo da correção de uma tela preta inicial. As causas investigadas e corrigidas incluíram: (1) ausência de código de desenho na função `display`, (2) configuração incorreta de matrizes e iluminação na função `init`, e (3) implementação de uma rotina de auto-escala e centralização baseada na Bounding Box do modelo para garantir que o objeto estivesse visível na câmera.
*   **Compatibilidade de Ambiente:** O programa foi testado em um ambiente Arch Linux com o compositor Hyprland (Wayland). A renderização com GLUT funcionou corretamente após as correções no código, indicando que os problemas iniciais não estavam relacionados ao ambiente, mas a erros de implementação e, posteriormente, a dados de modelo específicos.
*   **Limitações e Melhorias Futuras:** O renderizador atual utiliza o modo imediato do OpenGL (`glBegin`/`glEnd`), que é uma abordagem antiga e com baixo desempenho para modelos com alta contagem de polígonos, como o `dragon.obj` (mais de 870.000 faces). Uma futura melhoria seria migrar para o modo retido (moderno) utilizando *Vertex Buffer Objects* (VBOs) para um desempenho de renderização drasticamente superior.

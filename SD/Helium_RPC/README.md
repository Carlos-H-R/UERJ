Helium_RPC

Helium_RPC é uma implementação simplificada de um sistema de Chamada de Procedimento Remoto (RPC) em Python. Ele permite que programas cliente executem funções em um servidor remoto de forma transparente, como se estivessem chamando funções locais. O sistema inclui um "binder" (serviço de registro) para descoberta de serviços, um servidor RPC para hospedar serviços e um cliente RPC com um gerador de stubs dinâmico.
Estrutura do Projeto

O projeto está organizado nas seguintes pastas:

    interface/: Contém as definições de serviço (ex: math_service.py).

    rpc/: Contém os componentes principais do sistema RPC (servidor, cliente, binder, serializador, gerador de stubs).

    examples/: Contém exemplos de como usar o servidor e o cliente RPC.

Componentes Principais
rpc/rpc_server.py

O rpc_server é responsável por:

    Iniciar o servidor RPC e escutar por conexões de clientes.

    Registrar os serviços disponíveis (como math_service) com o binder.

    Processar requisições de RPC recebidas dos clientes, executando o método solicitado e retornando o resultado.

    Cada serviço e cada requisição de cliente são tratados em threads separadas para permitir processamento concorrente.

rpc/rpc_client.py

O rpc_client é a base para a comunicação do lado do cliente. Ele:

    Conecta-se ao binder para localizar o endereço de um serviço remoto.

    Estabelece uma conexão com o servidor que hospeda o serviço desejado.

    Serializa as chamadas de método e seus argumentos, envia-os ao servidor e desserializa o resultado.

rpc/rpc_binder.py

O binder atua como um serviço de registro central no sistema RPC. Suas funções incluem:

    Permitir que os servidores registrem seus serviços, associando um nome de serviço a um endereço IP e porta.

    Permitir que os clientes consultem (lookup) o endereço de um serviço pelo seu nome.

    Gerencia as conexões de registro e lookup em threads separadas.

rpc/rpc_stub_generator.py

O rpc_stub_generator é um componente inteligente que cria "stubs" dinamicamente. Ele:

    Permite que o código cliente chame métodos remotos como se fossem métodos locais.

    Intercepta chamadas a métodos não existentes e as redireciona para o rpc_client, que então as envia para o servidor remoto. Isso abstrai a complexidade da comunicação RPC do desenvolvedor.

rpc/serializer.py

A classe serializer é fundamental para a comunicação entre os componentes RPC. Ela:

    Converte objetos Python (como requisições de método e resultados) em um formato de bytes para transmissão pela rede (usando pickle).

    Converte os bytes recebidos de volta em objetos Python.

    Gerencia a formatação e a análise de protocolos de comunicação (REGISTER, LOOKUP, END).

interface/math_service.py

Este arquivo define um exemplo de serviço que pode ser exposto via RPC.

    A classe math_service contém métodos para operações matemáticas básicas como adição, subtração, divisão e multiplicação.

    É um exemplo de como você pode estruturar seus próprios serviços para serem disponibilizados através do sistema Helium_RPC.

Como Usar

Para executar o sistema Helium_RPC e testar os exemplos, siga os passos abaixo:
Pré-requisitos

    Python 3.x instalado.

Configuração do Ambiente

    Navegue até a pasta raiz do projeto Helium_RPC:

    cd /caminho/para/Helium_RPC

    Adicione o diretório pai ao PYTHONPATH (necessário para as importações relativas):
    Os scripts de exemplo e os componentes RPC já incluem linhas para adicionar o diretório pai ao sys.path. Certifique-se de que estas linhas estão presentes e corretas no topo dos seus scripts:

    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))

Executando os Componentes

Você precisará executar o binder, o server e o client em terminais separados.

    Iniciar o Binder:
    Abra um terminal e execute o script do binder:

    python rpc/rpc_binder.py

    Você deverá ver a mensagem: Binder Online ...

    Iniciar o Servidor RPC:
    Abra um novo terminal e execute o script do servidor:

    python examples/server_example.py

    No terminal do binder, você verá mensagens de registro de serviço. No terminal do servidor, você verá: >> Server Online!

    Executar o Cliente RPC:
    Abra um terceiro terminal e execute o script do cliente:

    python examples/client_example.py

    Você verá os resultados das operações matemáticas impressos no terminal do cliente. No terminal do servidor, você verá mensagens de requisição de serviço.

Fluxo de Operação

    Início do Binder: O rpc_binder.py inicia e fica aguardando conexões.

    Início do Servidor: O rpc_server.py inicia, cria instâncias de seus serviços (ex: math_service), e para cada serviço:

        Cria um socket de serviço dedicado em uma porta dinâmica.

        Inicia uma thread para escutar por requisições nesse socket.

        Envia uma mensagem REGISTER para o binder, informando seu nome de serviço e endereço (IP:Porta).

    Início do Cliente: O client_example.py cria um rpc_stub_generator. Quando um método como math_stub.add() é chamado:

        O rpc_stub_generator intercepta a chamada e usa o rpc_client.

        O rpc_client envia uma mensagem LOOKUP para o binder, solicitando o endereço do serviço 'add'.

        O binder responde com o endereço do servidor que hospeda o serviço 'add'.

        O rpc_client conecta-se diretamente ao servidor de serviço.

        A requisição (nome do método e argumentos) é serializada e enviada ao servidor.

        O servidor processa a requisição, executa o método add da math_service, serializa o resultado e o envia de volta ao cliente.

        O rpc_client desserializa o resultado e o retorna ao rpc_stub_generator, que por sua vez o retorna ao código cliente.

Este README fornece uma visão geral completa do projeto Helium_RPC, seus componentes e como executá-lo.
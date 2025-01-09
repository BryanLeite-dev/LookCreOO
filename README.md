Gerenciador de Armário

Descrição

O Gerenciador de Armário é uma aplicação desenvolvida em Python utilizando a biblioteca Tkinter para criar uma interface gráfica intuitiva. Ele permite gerenciar itens de vestuário e looks, além de carregar e salvar os dados em arquivos JSON. A interface é dividida em abas para facilitar a navegação e organização das funcionalidades.

Funcionalidades

Aba "Itens"

Adicionar Item: Adiciona uma nova roupa ao armário com detalhes como nome, tipo, tamanho, cor, tecido e estilo.

Listar Itens: Exibe uma lista de todos os itens cadastrados no armário.

Buscar Item: Permite buscar um item específico pelo nome.

Editar Item: Atualiza as informações de um item existente.

Remover Item: Remove um item do armário e exclui todos os looks associados a ele.

Aba "Looks"

Criar Look: Cria um novo look combinando itens existentes no armário.

Listar Looks: Exibe uma lista de todos os looks criados.

Buscar Look: Permite buscar um look específico pelo nome.

Editar Look: Atualiza as informações de um look existente.

Remover Look: Remove um look do armário.

Aba "Gerenciamento"

Salvar Armário em JSON: Exporta os itens e looks do armário para um arquivo JSON.

Carregar Armário de JSON: Importa itens e looks de um arquivo JSON para o armário.

Requisitos

Python 3.7 ou superior

Bibliotecas Python:

Tkinter (incluída por padrão na instalação do Python)

JSON (incluída por padrão na instalação do Python)

Como Executar

Clone ou baixe este repositório.

Navegue até o diretório do projeto no terminal.

Execute o seguinte comando:

python LookCre.py

A interface do Gerenciador de Armário será exibida.

Layout da Interface

A interface é composta por um Notebook com três abas:

Itens: Focado no gerenciamento de roupas individuais.

Looks: Voltado para a criação e edição de combinações.

Gerenciamento: Para carregar e salvar o armário em arquivos JSON.

A janela abre centralizada na tela para melhorar a experiência do usuário.

Estrutura do Projeto

LookCre.py: Arquivo principal contendo a lógica do armário, interface gráfica e manipulação de arquivos JSON.

Melhorias Futuras

Adição de filtros para busca de itens e looks.

Visualização de looks com imagens dos itens.

Integração com banco de dados para armazenamento persistente.



Bontempo – Sistema de Gestão de Consultórios

1. Apresentação

O Bontempo é um sistema web desenvolvido como projeto acadêmico, com a finalidade de facilitar a organização e o gerenciamento das atividades de um consultório.
A ideia do projeto surgiu da necessidade de reunir informações importantes em um único lugar, facilitando o controle de pacientes, profissionais, especialidades e consultas.
Com o sistema, buscamos tornar essas atividades mais organizadas e simplificar o acesso às informações.

2. Tecnologias utilizadas

Durante o desenvolvimento do projeto, foram utilizadas as seguintes tecnologias:

- Python: linguagem utilizada no desenvolvimento.
- Streamlit: criação da interface do sistema.
- Xano: backend e gerenciamento dos dados.
- Git: controle de versões.
- GitHub: armazenamento e compartilhamento do projeto.

3. Acesso ao aplicativo
O sistema pode ser executado localmente seguindo as etapas abaixo.
Como executar o projeto:
1. Faça o download ou clone do repositório:
git clone https://github.com/thaistavares-coder/projetobontempo.git
2. Entre na pasta do projeto:
cd projetobontempo
3. Acesse a pasta frontend:
cd frontend
4. Instale as dependências:
pip install -r requirements.txt
5. Inicie o sistema:
python -m streamlit run app.py
6. Após a inicialização, abra no navegador o endereço informado pelo Streamlit.
O acesso local normalmente é feito por:
http://localhost:8501

4. Perfis de usuários
O sistema foi pensado para atender às necessidades administrativas de um consultório.
Entre as principais atividades estão:

- Gerenciamento dos pacientes.
- Cadastro e consulta de profissionais.
- Organização das especialidades.
- Controle e acompanhamento das consultas.
As permissões específicas dependem dos recursos de acesso implementados na versão final do sistema.

5. Funcionalidades
5.1. Dashboard
É a tela inicial do sistema, utilizada para facilitar a navegação entre os módulos e apresentar as informações disponíveis.
5.2. Pacientes
Nesse módulo é possível realizar o gerenciamento dos pacientes, incluindo:
- Cadastro de novos pacientes.
- Visualização dos pacientes cadastrados.
- Pesquisa de registros.
- Edição de informações.
- Exclusão de registros, quando disponível.
5.3. Profissionais
Permite cadastrar e consultar os profissionais que fazem parte do consultório, mantendo suas informações organizadas.
5.4. Especialidades
Área destinada ao gerenciamento das especialidades, permitindo organizar as áreas de atuação dos profissionais.
5.5. Consultas
Esse módulo permite organizar os atendimentos realizados pelo consultório.
As informações podem envolver:
- Paciente.
- Profissional responsável.
- Especialidade.
- Data e horário da consulta.
O sistema também possui recursos de visualização das consultas por meio de tabelas, cards e calendário, conforme as funcionalidades disponíveis.

6. Manual de utilização
6.1. Acessando o sistema
1. Inicie o aplicativo pelo Streamlit.
2. Abra o endereço disponibilizado no navegador.
3. Aguarde o carregamento da página inicial.
4. Utilize o menu lateral para acessar os módulos.
6.2. Cadastro de pacientes
1. Acesse a opção Pacientes.
2. Clique no botão de novo cadastro.
3. Preencha as informações solicitadas.
4. Confira os dados.
5. Clique em salvar.
6. Verifique se o paciente aparece na listagem.
6.3. Cadastro de profissionais
1. Acesse o módulo Profissionais.
2. Selecione a opção de cadastro.
3. Preencha os campos solicitados.
4. Informe a especialidade, quando necessário.
5. Salve o cadastro.
6. Confira se o profissional aparece na listagem.
6.4. Especialidades
1. Acesse o módulo Especialidades.
2. Visualize as especialidades cadastradas.
3. Utilize as opções disponíveis para gerenciar os registros.
6.5. Cadastro de consultas
1. Entre no módulo Consultas.
2. Clique na opção de novo agendamento.
3. Selecione o paciente.
4. Escolha o profissional responsável.
5. Preencha as informações da consulta.
6. Informe a data e o horário.
7. Salve o agendamento.
8. Confira se a consulta aparece na listagem ou calendário.
6.6. Edição e consulta de registros
1. Entre no módulo desejado.
2. Localize o registro que deseja consultar.
3. Utilize a pesquisa ou os filtros disponíveis.
4. Selecione a opção de edição, quando disponível.
5. Faça as alterações necessárias.
6. Salve e confira as informações atualizadas.

7. Como o sistema funciona
O Bontempo foi desenvolvido utilizando uma estrutura de frontend e backend.
O frontend foi construído em Python com Streamlit, responsável pelas telas, formulários, tabelas e demais elementos utilizados pelo usuário.
Para o backend, foi utilizada a plataforma Xano, responsável pelo armazenamento e gerenciamento das informações por meio de APIs.
A comunicação entre essas duas partes permite que as informações inseridas no sistema sejam enviadas ao backend e posteriormente consultadas e atualizadas pela aplicação.

8. Estrutura do projeto
O repositório está organizado em pastas para facilitar

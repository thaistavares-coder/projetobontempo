# Frontend Streamlit

## Requisitos

- Python 3.12 (versão verificada: 3.12.4)

## Executar localmente

Na raiz do repositório, crie e ative um ambiente virtual:

```powershell
python -m venv frontend/.venv
.\frontend\.venv\Scripts\Activate.ps1
```

Instale as dependências e inicie a aplicação:

```powershell
python -m pip install -r frontend/requirements.txt
python -m streamlit run frontend/app.py --server.address 127.0.0.1 --server.port 8502
```

O servidor fica limitado à máquina local e não escuta na rede.

## Integração Xano

As páginas de Pacientes e Profissionais usam exclusivamente o cliente HTTP em
`frontend/services/xano.py`; não consultam nem gravam esses módulos no SQLite.
O CRUD inclui listagem, leitura individual para edição, criação, atualização e
exclusão com confirmação explícita. A especialidade do profissional continua
como campo textual.

O cliente possui os grupos base confirmados como valores padrão, que podem ser
sobrescritos externamente por:

- `XANO_PACIENTES_BASE_URL`
- `XANO_PROFISSIONAIS_BASE_URL`

As rotas confirmadas são `/pacientes`, `/paciente/{paciente_id}`,
`/profissionais` e `/profissional/{profissional_id}`; o cliente usa as rotas de
coleção para GET/POST e as rotas individuais para GET/PATCH/DELETE. O campo de
identificação nas respostas é `id`. DELETE só é considerado bem-sucedido quando
a API retorna `{"success": true}`. `XANO_AUTHORIZATION` só deve ser configurada
se a autenticação dos endpoints exigir esse cabeçalho.

Por segurança, todas as chamadas de ambas as páginas ficam desabilitadas até
`XANO_API_ENABLED=true`. Sem habilitação, a interface explica o bloqueio e não
consulta o SQLite como alternativa. Erros HTTP, de rede, de configuração ou
respostas incompatíveis são exibidos sem serem convertidos em sucesso ou lista
vazia. Campos textuais são validados e normalizados antes do envio; email é
opcional e validado quando informado.

O endpoint remoto de criação de Pacientes chama `validar_telefone_paciente`,
que retorna `{valid: boolean}`, mas não verifica o resultado antes de gravar.
Essa inconsistência permanece pendente e não foi alterada nesta implementação.

Os testes automatizados substituem o cliente por mocks ou usam transporte
simulado; nenhuma requisição real ao Xano é feita pela suíte.

### Validação real de leitura

Em 2026-10-27, foi feita uma validação manual somente de leitura no ambiente
local, habilitando `XANO_API_ENABLED=true` apenas no processo de verificação.
Não havia overrides das URLs base nem cabeçalho de autorização configurados;
foram usados os defaults confirmados no cliente. A configuração não foi
persistida no ambiente nem em arquivos.

- GET da coleção de Pacientes: HTTP 200; resposta em lista com 9 registros;
  os campos foram aceitos pelo contrato do cliente.
- GET da coleção de Profissionais: HTTP 200; resposta em lista com 2 registros;
  os campos foram aceitos pelo contrato do cliente.
- As duas páginas foram executadas com `AppTest`: uma tabela carregada em cada
  página, sem exceções nem erros de interface; cada execução fez apenas um GET,
  com HTTP 200.
- Nenhum valor de registro foi incluído nesta documentação ou nos logs da
  verificação. Nenhuma operação POST, PATCH ou DELETE foi enviada.

Esta verificação confirma a leitura e a compatibilidade das listagens, mas não
valida operações de escrita, autenticação para essas operações nem o CRUD
remoto completo. A flag volta a ficar desabilitada fora do processo de teste.

### Validação real de escrita autorizada (parcial)

Em 2026-10-27, a página Streamlit foi exercitada com chamadas reais, usando
somente GET, POST e PATCH e dados sintéticos identificáveis. A integração foi
habilitada apenas no processo local de teste. Nenhum DELETE foi executado.

- Pacientes: POST HTTP 200 criou o registro sintético ID 19; GET por ID retornou
  HTTP 200; PATCH pela página retornou HTTP 200; GET por ID e GET da coleção
  retornaram HTTP 200 e confirmaram o campo atualizado no mesmo registro.
- Profissionais: o POST retornou HTTP 429 (Too Many Requests), sem ID de criação
  confirmado. A sequência foi interrompida: não houve GET por ID nem PATCH para
  Profissionais. Não foi feita nova tentativa; não se pode confirmar se o Xano
  chegou a persistir algo apesar da resposta 429.
- Os dados enviados eram fictícios. Nenhum conteúdo de registros preexistentes
  foi copiado para logs ou documentação.

A validação CRUD remota permanece incompleta até resolver a resposta 429 e
validar Profissionais com ID retornado pela própria criação. A exclusão dos
registros sintéticos permanece pendente de autorização específica.

## Persistência legada durante a migração

SQLite é apenas uma implementação legada temporária, não parte da arquitetura
oficial. Pacientes e Profissionais serão migrados para APIs Xano; Especialidades
e Consultas ainda dependem do serviço SQLite até suas próprias etapas de
migração. Nenhuma nova funcionalidade SQLite deverá ser adicionada. Após migrar
todos os módulos, uma etapa posterior removerá o serviço, a inicialização e as
dependências SQLite. O arquivo `frontend/data/bontempo_demo.sqlite3` não é
removido nem importado automaticamente.

Consultas locais usam `America/Sao_Paulo` como fuso da interface e persistem
instantes em UTC. Agendamentos e confirmações ocupam horário; intervalos
adjacentes são permitidos e consultas canceladas/realizadas/não comparecidas
liberam o horário.

## Testes

Execute os testes locais e os testes do cliente HTTP com transporte simulado,
a partir da pasta `frontend`:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Os testes não enviam requisições à rede e usam somente registros sintéticos.

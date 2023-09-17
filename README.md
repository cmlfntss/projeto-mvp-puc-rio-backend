# projeto-mvp-puc-rio-backend
Projeto para entrega da MVP da Pós Graduação Engenharia de Software da Instituição PUC-RIO

# API Lista de Tarefas Diárias

Lista de Tarefas : API tem como função disponibilizar a consulta de tarefas (caso tenha já cadastradas), criação, edição e exclusão. Single page application (SPA) consumindo o dado de uma API em vez do acesso aos dados estáticos de um arquivo JSON.

---
## Como instalar e executar a API


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(venv)$ pip install -r requirements.txt
```

REQUISITOS:

Realizar a instalação das libs python listadas no requirements.txt.
É recomendado o uso de ambientes virtuais do tipo virtualenv.

1 - Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo:
cd projeto-mvp-puc-rio-backend.git

2 - Instalar Virtualenv
$ pip install VirtualEnv

3 - Criar Virtualenv
$ Virtualenv venv

4 - Ativar venv
$ .\venv\Scripts\activate

5 - Instalar libs python, rodar o comando no terminal powershell
(venv)$ pip install -r requirements.txt

6 - Instalar Greenlet
(venv)$ pip install greenlet

7 - Executar API:
(venv)$ flask run --host 0.0.0.0 --port 5000
Em caso de modificações no código enquanto a API estiver rodando, utilizar o parâmetro reload, que reiniciará o servidor automaticamente após uma mudança no código fonte.

(venv)$ flask run --host 0.0.0.0 --port 5000 --reload
Após seguir todos os passos, abrir o link abaixo no bavegador para verificar o status da API em execução

8 - Acesse a API em seu navegador:

http://127.0.0.1:5000/

Documentação Swagger
A documentação Swagger da API pode ser acessada em:

http://127.0.0.1:5000/api/swagger/

Link do vídeo postado no [YouTube](https://youtu.be/sF8-KFsaOOc)

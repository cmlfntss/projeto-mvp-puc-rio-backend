import sqlite3
import os
from flask import Flask, render_template, request, url_for, redirect, g
from flask_restx import Api, Resource, fields, reqparse

app = Flask(__name__, template_folder='../frontend/templates')
api = Api(
    app,
    version='1.0',
    title='Minha API de Tarefas',
    description='Uma API para criar, editar e excluir tarefas',
)

# Modelo para tarefa
parser = reqparse.RequestParser()
parser.add_argument('tarefa', type=str)

# Conexão com o banco de dados SQLite
def connect_to_database():
    db_path = os.path.join(os.path.dirname(__file__), 'listapendencias.db')
    sql = sqlite3.connect(db_path)
    sql.row_factory = sqlite3.Row
    return sql

# Função para obter o banco de dados
def get_database():
    if not hasattr(g, "listapendencias_db"):
        g.listapendencias_db = connect_to_database()
    return g.listapendencias_db

# Defina a classe para sua API
@api.route('/api/tarefas')
class TarefaList(Resource):
    @api.doc(
        description='Lista todas as tarefas',
        responses={200: 'Success', 400: 'Validation Error'}
    )
    def get(self):
        """Lista todas as tarefas"""
        db = get_database()
        tarefas_cursor = db.execute("select * from lista")
        todastarefas = [dict(row) for row in tarefas_cursor.fetchall()]  # Converta para lista de dicionários
        db.close()
        return todastarefas

    @api.doc(
        description='Adiciona uma nova tarefa',
        responses={201: 'Created', 400: 'Validation Error'},
        params={'tarefa': 'A tarefa a ser adicionada'}
    )
    def post(self):
        """Adiciona uma nova tarefa"""
        args = parser.parse_args()
        new_task = args['tarefa']
        db = get_database()
        db.execute("insert into lista (tarefas) values (?)", [new_task])
        db.commit()
        db.close()
        return {'message': 'Tarefa adicionada com sucesso'}, 201

@api.route('/api/tarefas/<int:id>')
class Tarefa(Resource):
    @api.doc(
        description='Obtém uma tarefa por ID',
        responses={200: 'Success', 400: 'Validation Error'},
        params={'id': 'ID da tarefa'}
    )
    def get(self, id):
        """Obtém uma tarefa por ID"""
        db = get_database()
        cursor = db.cursor()
        cursor.execute("SELECT tarefas FROM lista WHERE id = ?", (id,))
        task = cursor.fetchone()
        db.close()

        if task:
            return task[0]
        else:
            return {'message': 'Tarefa não encontrada'}, 404

    @api.doc(
        description='Edita uma tarefa por ID',
        responses={200: 'Success', 400: 'Validation Error'},
        params={'id': 'ID da tarefa', 'tarefa': 'Nova tarefa'}
    )
    def put(self, id):
        """Edita uma tarefa por ID"""
        args = parser.parse_args()
        edited_task = args['tarefa']
        db = get_database()
        db.execute("UPDATE lista SET tarefas = ? WHERE id = ?", (edited_task, id))
        db.commit()
        db.close()
        return {'message': 'Tarefa editada com sucesso'}

    @api.doc(
        description='Exclui uma tarefa por ID',
        responses={204: 'No Content', 400: 'Validation Error'},
        params={'id': 'ID da tarefa'}
    )
    def delete(self, id):
        """Exclui uma tarefa por ID"""
        db = get_database()
        db.execute("DELETE FROM lista WHERE id = ?", (id,))
        db.commit()
        db.close()
        return {'message': 'Tarefa excluída com sucesso'}

# Rota de especificação Swagger
@api.route('/api/spec')
class SwaggerSpec(Resource):
    @api.doc(
        description='Exibe a especificação Swagger da API',
        responses={200: 'Success'}
    )
    def get(self):
        """Exibe a especificação Swagger da API"""
        return api.__schema__

# Seu código de rota existente
@app.route('/', methods=["POST", "GET"])
def index():
    db = get_database()
    tarefas_cursor = db.execute("select * from lista")
    todastarefas = [dict(row) for row in tarefas_cursor.fetchall()]  # Converta para lista de dicionários
    db.close()
    return render_template("index.html", todastarefas=todastarefas)

@app.route('/inserirtarefa', methods=["POST", "GET"])
def inserirtarefa():
    if request.method == "POST":
        # Obtem a tarefa inserida pelo usuário no formulário.
        enteredtask = request.form['tarefasdiarias']
        db = get_database()
        db.execute("insert into lista (tarefas) values (?)", [enteredtask])
        db.commit()
        db.close()
        return redirect(url_for("index"))
    return render_template("index.html")

@app.route('/editartarefa/<int:id>', methods=["GET", "POST"])
def editartarefa(id):
    db = get_database()
    cursor = db.cursor()

    if request.method == "POST":
        # Obtenha a tarefa editada do formulário.
        edited_task = request.form['edited_task']

        # Atualize a tarefa no banco de dados.
        cursor.execute("UPDATE lista SET tarefas = ? WHERE id = ?", (edited_task, id))
        db.commit()
        db.close()
        return redirect(url_for("index"))

    cursor.execute("SELECT tarefas FROM lista WHERE id = ?", (id,))
    task = cursor.fetchone()
    db.close()

    if task:
        return render_template("editartarefa.html", task=task[0])
    else:
        # Lida com o caso em que o ID da tarefa não existe.
        return "Tarefa não encontrada", 404

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, url_for, redirect
from database import get_database, connect_to_database
from flask_restx import Api, Namespace, Resource, fields

app = Flask(__name__, template_folder='../frontend-puc/templates')

@app.route('/', methods=["POST", "GET"])
def index():
    """
    Lista todas as tarefas.
    """
    db = get_database()
    task_cursor = db.execute("SELECT * FROM listadetarefas")
    todasastarefas = task_cursor.fetchall()
    return render_template("index.html", todasastarefas=todasastarefas)

@app.route('/inserirtarefas', methods=["POST", "GET"])
def inserirtarefas():
    """
    Insere uma nova tarefa.
    """
    if request.method == "POST":
        enteredtask = request.form['tarefadehoje']
        db = get_database()
        db.execute("INSERT INTO listadetarefas (tarefa) VALUES (?);", [enteredtask])
        db.commit()
        return redirect(url_for("index"))
    return render_template("index.html")

@app.route('/editartarefa/<int:id>', methods=["GET", "POST"])
def editartarefa(id):
    """
    Edita uma tarefa existente.
    """
    db = get_database()
    cursor = db.cursor()

    if request.method == "POST":
        edited_task = request.form['edited_task']
        task_id = request.form['task_id']
        cursor.execute("UPDATE listadetarefas SET tarefa = ? WHERE id = ?", (edited_task, task_id))
        db.commit()
        return redirect(url_for("index"))

    cursor.execute("SELECT tarefa FROM listadetarefas WHERE id = ?", (id,))
    task = cursor.fetchone()
    db.close()

    if task:
        return render_template("editartarefa.html", task=task[0], task_id=id)
    else:
        return "Tarefa não encontrada", 404

@app.route("/deletartarefas/<int:id>", methods=["POST", "GET"])
def deletartarefas(id):
    """
    Deleta uma tarefa existente.
    """
    if request.method == "GET":
        db = get_database()
        db.execute("DELETE FROM listadetarefas WHERE id = (?);", [id])
        db.commit()
        return redirect(url_for("index"))
    return render_template("index.html")

# Configuração da API Flask-RESTx
api = Api(app,
          title="LISTA DE TAREFAS",
          description="Documentação da Lista de Tarefas",
          version="1.0",
          doc="/api/swagger/",
          validate=True
          )

# Namespace para as operações da API
ns = Namespace('tarefas', description='API Controller da Lista de Tarefas')

# Modelo para a representação da tarefa
task_model = api.model('Task', {
    'id': fields.Integer(readonly=True, description='ID da tarefa'),
    'tarefa': fields.String(required=True, description='Descrição da tarefa')
})

# Recurso para listar todas as tarefas
@ns.route('/listadetarefas')
class TaskListResource(Resource):

    @ns.marshal_list_with(task_model)
    def get(self):
        """
        Lista todas as tarefas.
        """
        db = get_database()
        task_cursor = db.execute("SELECT * FROM listadetarefas")
        todasastarefas = task_cursor.fetchall()
        return todasastarefas

    @ns.expect(task_model)
    @ns.marshal_with(task_model, code=201)
    def post(self):
        """
        Insere uma nova tarefa.
        """
        entered_task = api.payload['tarefa']
        db = get_database()
        db.execute("INSERT INTO listadetarefas (tarefa) VALUES (?);", [entered_task])
        db.commit()
        return {'tarefa': entered_task}, 201

# Recurso para deletar uma tarefa
@ns.route('/deletartarefa')
class DeleteTaskResource(Resource):

    @ns.expect(task_model)
    @ns.marshal_with(task_model)
    def delete(self):
        """
        Deleta uma tarefa.
        """
        entered_task = api.payload['tarefa']
        db = get_database()
        db.execute("DELETE FROM listadetarefas WHERE tarefa = ?;", [entered_task])
        db.commit()
        return {'tarefa': entered_task}

api.add_namespace(ns)

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)

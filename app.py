from flask import Flask, render_template, request, url_for, redirect
from database import get_database, connect_to_database

# app = app = Flask (__name__, template_folder='../frontend-puc/templates')

app = Flask(__name__, template_folder='../frontend-puc/templates')



@app.route('/', methods = ["POST", "GET"])
def index():
    db = get_database()
    task_cursor = db.execute("select * from listadetarefas")
   
    todasastarefas = task_cursor.fetchall()

    return render_template("index.html", todasastarefas = todasastarefas)

@app.route('/inserirtarefas', methods=["POST", "GET"])
def inserirtarefas():
    if request.method == "POST":
        enteredtask = request.form['tarefadehoje']  
        db = get_database()
        db.execute("insert into listadetarefas ( tarefa) values (?);", [enteredtask])
        db.commit()
        return redirect(url_for("index"))
    return render_template("index.html")

@app.route('/editartarefa/<int:id>', methods=["GET", "POST"])
def editartarefa(id):
    db = get_database()
    cursor = db.cursor()

    if request.method == "POST":
        # Obtenha a tarefa editada do formulário.
        edited_task = request.form['edited_task']
        task_id = request.form['task_id']

        # Atualize a tarefa no banco de dados com base no task_id.
        cursor.execute("UPDATE listadetarefas SET tarefa = ? WHERE id = ?", (edited_task, task_id))
        db.commit()
        return redirect(url_for("index"))

    # Se o método for GET, exiba o formulário de edição.
    cursor.execute("SELECT tarefa FROM listadetarefas WHERE id = ?", (id,))
    task = cursor.fetchone()
    db.close()

    if task:
        return render_template("editartarefa.html", task=task[0], task_id=id)
    else:
        # Lida com o caso em que o ID da tarefa não existe.
        return "Tarefa não encontrada", 404
    
@app.route("/deletartarefas/<int:id>", methods = ["POST", "GET"])
def deletartarefas(id):
    if request.method == "GET":
        db = get_database()
        db.execute("delete from listadetarefas where id =  (?);", [id])
        db.commit()
        return redirect(url_for("index"))
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)
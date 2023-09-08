from flask import Flask, render_template, request, url_for, redirect
from database import get_database, connect_to_database

app = Flask (__name__, template_folder='../frontend/templates')


@app.route('/', methods=["POST", "GET"])
def index():
    db = get_database()
    tarefas_cursor = db.execute("select * from lista")

    todastarefas = tarefas_cursor.fetchall()

    return render_template("index.html", todastarefas = todastarefas)


@app.route('/inserirtarefa', methods=["POST", "GET"])
def inserirtarefa():
    if request.method == "POST":
        # obtem a tarefa inserida pelo usuário no formulário.
        enteredtask = request.form['tarefasdiarias']
        db = get_database()
        db.execute("insert into lista ( tarefas) values (?)", [enteredtask])
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

        # Atualize a tarefa no banco de dados.
        cursor.execute("UPDATE lista SET tarefas = ? WHERE id = ?", (edited_task, id))
        db.commit()

        return redirect(url_for("index"))

    # Se o método for GET, exiba o formulário de edição.
    cursor.execute("SELECT tarefas FROM lista WHERE id = ?", (id,))
    task = cursor.fetchone()
    db.close()

    if task:
        return render_template("editartarefa.html", task=task[0])
    else:
        # Lida com o caso em que o ID da tarefa não existe.
        return "Tarefa não encontrada", 404

@app.route("/deletartarefa/<int:id>", methods=["POST", "GET"])
def deletartarefa(id):
    if request.method == "GET":
        db = get_database()
        db.execute("delete from lista where id = ?", [id])
        db.commit()
        return redirect(url_for("index"))
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
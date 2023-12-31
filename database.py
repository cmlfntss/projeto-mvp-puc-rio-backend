import sqlite3
import os
from flask import g

def connect_to_database():
    db_path = os.path.join(os.path.dirname(__file__), 'apptarefas.db')
    sql = sqlite3.connect(db_path)
    sql.row_factory = sqlite3.Row
    return sql

def get_database():
    if not hasattr(g, "apptarefas_db"):
        g.apptarefas_db = connect_to_database()
    return g.apptarefas_db
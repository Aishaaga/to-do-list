from flask import Flask, render_template, request, redirect
import sqlite3

# Initialisation de l'application Flask
app = Flask(__name__)

# Fonction pour se connecter à la base de données
def connect_db():
    return sqlite3.connect('todo.db')

# Route pour afficher les tâches
@app.route('/')
def index():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, task FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# Route pour ajouter une tâche
@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    if task:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
        conn.commit()
        conn.close()
    return redirect('/')

# Route pour supprimer une tâche
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

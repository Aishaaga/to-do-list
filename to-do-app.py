

from flask import Flask, render_template, request, redirect, jsonify, flash
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Fonction pour obtenir une connexion MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",       # Mets ton utilisateur MySQL
        password="",       # Mets ton mot de passe MySQL
        database="todolist"
    )

@app.route('/')
def index():
    today = datetime.today().strftime('%Y-%m-%d')
    now = datetime.now().strftime('%H:%M')

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT id, task, due_date, task_time, priority, completed FROM tasks ORDER BY priority ASC, due_date ASC")
    tasks = cursor.fetchall()
    cursor.close()
    db.close()
    
    return render_template('index.html', tasks=tasks, today=today, now=now)


@app.route('/add', methods=['POST'])
def add_task():
    task_text = request.form['task']
    due_date = request.form.get('due_date')
    task_time = request.form['task_time']
    priority = int(request.form['priority'])  # Récupérer la priorité choisie

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO tasks (task, due_date, task_time, priority) VALUES (%s, %s, %s, %s)", 
                   (task_text, due_date, task_time, priority))
    db.commit()  
    cursor.close()
    db.close()
    return redirect('/')



app.secret_key = 'your_secret_key'  # Nécessaire pour utiliser flash()

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT task FROM tasks WHERE id = %s", (task_id,))
    task_name = cursor.fetchone()  # Récupère le nom de la tâche avant de la supprimer

    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    db.commit()  
    cursor.close()
    db.close()

    if task_name:
        flash(f'Tâche "{task_name[0]}" supprimée !', 'info')  # Message temporaire

    return redirect('/')



@app.route('/update', methods=['POST'])
def update_task():
    data = request.get_json()
    task_id = data.get('task_id')
    is_completed = data.get('completed')

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE tasks SET completed = %s WHERE id = %s", (is_completed, task_id))
    db.commit()  
    cursor.close()
    db.close()

    return jsonify({'success': True})

    


if __name__ == '__main__':
    app.run(debug=True)

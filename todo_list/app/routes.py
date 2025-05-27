from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Task
from datetime import datetime, timedelta

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    task = Task(task=request.form['task'])
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        task.task = request.form['task']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', id=id, task=task)

@app.before_request
def delete_old_completed_tasks():
    threshold = datetime.utcnow() - timedelta(seconds=5)
    old_tasks = Task.query.filter(Task.completed == True, Task.completed_at != None, Task.completed_at < threshold).all()
    for task in old_tasks:
        db.session.delete(task)
    if old_tasks:
        db.session.commit()

@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    task = Task.query.get(task_id)
    if not task.completed:
        task.completed = True
        task.completed_at = datetime.utcnow()
    else:
        task.completed = False
        task.completed_at = None
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

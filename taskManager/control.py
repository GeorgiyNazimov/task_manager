from flask import Flask
from flask import render_template, request, redirect, url_for
from datetime import datetime
from sqlalchemy import select, delete, text

from model import db, Task

app = Flask(__name__)

#вставьте данные своей базы данных для подключения
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@adres/db'
db.init_app(app)

#отрисовка главной страницы
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

#обработка запроса на создание задачи
@app.route('/create', methods=['POST'])
def create_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        task = Task(title=title, description=description, created_date=datetime.utcnow())
        db.session.add(task)
        db.session.commit()
    return redirect(url_for('index'))

#обработка запроса на удаление задачи
@app.route('/delete', methods=['POST'])
def delete_task():
    ids = request.form.getlist('delete')
    if ids:
        stmt = delete(Task).where(Task.id.in_(ids))
        db.session.execute(stmt)
        db.session.commit()
    return redirect(url_for('index'))

#обработка запроса на удаление всех задач
@app.route('/clear', methods=['POST'])
def clear():
    stmt = (delete(Task).where(Task.id))
    db.session.execute(stmt)
    db.session.execute(text('alter table Task AUTO_INCREMENT = 1'))
    db.session.commit()
    return redirect(url_for('index'))

#запуск приложения
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
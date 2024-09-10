from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#схема таблицы задач(id, название, описание, дата создания)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
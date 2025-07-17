from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Electrician(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    skills = db.Column(db.String(200))
    rating = db.Column(db.Float, default=0.0)
    location = db.Column(db.String(100))
    availability = db.Column(db.Boolean, default=True)

class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300))
    location = db.Column(db.String(100))
    urgency = db.Column(db.String(50))
    electrician_id = db.Column(db.Integer, db.ForeignKey('electrician.id'))
    from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50))  # 'consumer' or 'electrician'
    class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float, nullable=False)
    comment = db.Column(db.String(300))
    electrician_id = db.Column(db.Integer, db.ForeignKey('electrician.id'))
    consumer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
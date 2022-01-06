from app import db

class User(db.Model):
    username=db.Column(db.String(50),primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    family_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, index=True)
    password=db.Column(db.String(200),nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))



class Role(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    role_name=db.Column(db.String(100),nullable=False)
    users=db.relationship('User',backref='role_name')
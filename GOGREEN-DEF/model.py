from app import db


class User(db.Model):
    __tablename__ = "users"
    email = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    family_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(100), nullable=False)
    users = db.relationship('User', backref='role_name')

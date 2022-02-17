from datetime import datetime

from app import db


class User(db.Model):
    __tablename__ = "users"
    email = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    family_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    date_of_registration = db.Column(db.DateTime, default=datetime.now())
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    transportations = db.relationship("Transportation", backref="user_tr")

    def get_date_of_registration(self):
        return self.date_of_registration.strftime("%Y-%m-%d")

    def get_password(self):
        return self.password


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(100), nullable=False)
    users = db.relationship('User', backref='role_name')


class SharingCompany(db.Model):
    __tablename__ = "sharing_companies"
    name = db.Column(db.String(50), primary_key=True)
    date_of_registration = db.Column(db.Date)
    num_vehicles = db.Column(db.Integer, nullable=False, default=1)
    price_per_minute = db.Column(db.Float, nullable=False)
    min_age = db.Column(db.Integer, nullable = False, default = 18)
    type_vehicle = db.Column(db.String(20), nullable = False)
    type_motor = db.Column(db.String(20), nullable = False)
    points = db.Column(db.Integer, nullable=False)
    transportations = db.relationship("Transportation", backref="sharing_company_tr")

    def to_string(self):
        s = str(str(self.price_per_minute) + " euro/minute")
        return s

class Transportation(db.Model):
    __tablename__ = "transportations"
    user = db.Column(db.String(100), db.ForeignKey('users.email'), primary_key=True)
    sharing_company = db.Column(db.String(50), db.ForeignKey('sharing_companies.name'), primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now(), primary_key=True)
    def getDate(self):
        s = self.date.strftime("%Y-%m-%d %H:%M:%S")
        return s

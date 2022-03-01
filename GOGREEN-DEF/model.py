from datetime import datetime

from app import db



class Flag():
    flag=False

    def getFlag(self):
        return self.flag

    def SetFlag(self, bool):
        if bool==True:
            self.flag=True
        else:
            self.flag = False

class User(db.Model):
    __tablename__ = "users"
    email = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    family_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    date_of_registration = db.Column(db.DateTime, default=datetime.now())
    transportations = db.relationship("Transportation", backref="user_tr")

    def get_date_of_registration(self):
        return self.date_of_registration.strftime("%Y-%m-%d")

    def get_password(self):
        return self.password

class Mean(db.Model):
    __tablename__ = "means"
    id = db.Column(db.Integer, primary_key=True)
    sharing_company = db.Column(db.String(100), db.ForeignKey('sharing_companies.name'), primary_key=True)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    transportations = db.relationship("Transportation", backref="transportation_id")


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
    reservation_time = db.Column(db.Time, nullable=False)
    transportations = db.relationship("Transportation", backref="sharing_company_tr")
    means = db.relationship("Mean", backref="sharing_company_mean")

    def to_string(self):
        s = str(str(self.price_per_minute) + " euro/minute")
        return s

class Transportation(db.Model):
    __tablename__ = "transportations"
    user = db.Column(db.String(100), db.ForeignKey('users.email'), primary_key=True)
    sharing_company = db.Column(db.String(50), db.ForeignKey('sharing_companies.name'), primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now(), primary_key=True)
    id = db.Column(db.Integer, db.ForeignKey('means.id'))
    def getDate(self):
        s = self.date.strftime("%Y-%m-%d %H:%M:%S")
        return s

class Rating(db.Model):
    __tablename__ = "ratings"
    user = db.Column(db.String(100), db.ForeignKey('users.email'), primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now(), primary_key=True)
    rank = db.Column(db.Integer)
    reason = db.Column(db.String(200))

class FinalFeedback(db.Model):
    __tablename__ = "final_feedback"
    user = db.Column(db.String(100),db.ForeignKey('users.email'), primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now())
    motivation = db.Column(db.Integer)
    other = db.Column(db.String(200))
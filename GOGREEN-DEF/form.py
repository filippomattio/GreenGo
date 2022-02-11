from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,FileField, DateField
from wtforms.validators import DataRequired, Length,ValidationError
from app import User, bcrypt
from flask import flash


class LoginForm(FlaskForm):
    email = StringField('E-Mail:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    email = StringField('E-Mail:', validators=[DataRequired()])
    name = StringField('Name:', validators=[DataRequired(), Length(min=3, max=10)])
    family_name = StringField('Family name:', validators=[DataRequired(), Length(min=3, max=10)])
    date_of_birth = StringField('Birthdate: ', validators=[DataRequired(), Length(min=10, max=10)])
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=3, max=10)])
    submit = SubmitField('Sign in')

    def validate_email(self, email):
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            flash("User with email %s already exists!" % self.email.data, 'errorEmail')
            return False
        else:
            return True

class ChangeForm(FlaskForm):
    old_password = PasswordField('Old Password:', validators=[DataRequired(), Length(min=3, max=10)])
    new_password = PasswordField('New Password:', validators=[DataRequired(), Length(min=3, max=10)])
    submit = SubmitField('Change Password')

    def validate_password(self, old_password, email):
        user = User.query.filter_by(email=email).first()
        if not user or not bcrypt.check_password_hash(old_password, self.old_password.data):
            raise ValidationError("Old password not correct!")

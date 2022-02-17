from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,FileField, DateField, RadioField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length,ValidationError
from app import User, bcrypt
from flask import flash
import re


class LoginForm(FlaskForm):
    email = StringField('E-Mail:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    email = StringField('E-Mail:', validators=[DataRequired()])
    name = StringField('Name:', validators=[DataRequired(), Length(min=3, max=10)])
    family_name = StringField('Family name:', validators=[DataRequired(), Length(min=3, max=10)])
    date_of_birth = DateField('Birthdate: ', validators=[DataRequired()], format='%Y-%m-%d')
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=3, max=10)])
    submit = SubmitField('Sign in')

    def validate_email(self, email):
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            flash("User with email ' %s ' already exists!" % self.email.data, 'errorEmail')
            return False
        else:
            return True
    def check_password(self, password):
        regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&-_])[A-Za-z\d@$!#%*?&-_]{8,20}$"
        if re.search(regex, password):
            return True
        else:
            flash('Password must be between 8 and 20 characters and must contains at least one capital letter and one number. Special characters are admitted', 'errorPassword')
            return False

    def check_email(self,email):
        regex = "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}"
        if re.search(regex, email):
            return True
        else:
            flash(
                'Email format not valid. Please, try again.',
                'errorEmail')
            return False


class ChangeForm(FlaskForm):
    old_password = PasswordField('Old Password:', validators=[DataRequired(), Length(min=3, max=10)])
    new_password = PasswordField('New Password:', validators=[DataRequired(), Length(min=3, max=10)])
    submit = SubmitField('Change Password')

    def validate_password(self, old_password, email):
        user = User.query.filter_by(email=email).first()
        if not user or not bcrypt.check_password_hash(old_password, self.old_password.data):
            flash("Old password not correct!", 'oldPassword')
            return False
        return True

class DeleteForm(FlaskForm):
    motivation = RadioField(choices=[('1','low user experience quality'), ('2','limitated number of sharing companies'),
    ('3','too much advertisements'), ('4', 'other')], default='4')
    other = TextAreaField('Other reasons', validators=[Length(max=200)], default="Please, explain here any bag of the app or any advice you want to give us")
    submit = SubmitField('Delete Account')

class FeedbackForm(FlaskForm):
    rank = SelectField('Rank', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')], validators=[DataRequired()])
    reason = TextAreaField('Other reasons', validators=[Length(max=200)],
                          default="Please, explain here any bag of the app or any advice you want to give us")
    submit = SubmitField('Send feedback')
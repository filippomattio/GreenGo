from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,FileField, DateField
from wtforms.validators import DataRequired, Length,ValidationError
from app import User

class LoginForm(FlaskForm):
    email = StringField('E-Mail', validators=[DataRequired()])
    password = PasswordField('Password:' ,validators=[DataRequired(),Length(min=3,max=10)])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    email = StringField('E-Mail', validators=[DataRequired()])
    name = StringField('Name:', validators=[DataRequired(), Length(min=3, max=10)])
    family_name = StringField('Family name:', validators=[DataRequired(), Length(min=3, max=10)])
    date_of_birth = StringField('Birthdate: ', validators=[DataRequired(), Length(min=10, max=10)])
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=3, max=10)])
    submit = SubmitField('Store')

    def validate_email(self, email):
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            raise ValidationError("User with email ' %s ' already exist!" % self.email.data)
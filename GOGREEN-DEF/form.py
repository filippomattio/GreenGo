from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,FileField
from wtforms.validators import DataRequired, Length,ValidationError

class LoginForm(FlaskForm):
    username = StringField('Username:',validators=[DataRequired(),Length(min=3,max=10)])
    password = PasswordField('Password:' ,validators=[DataRequired(),Length(min=3,max=10)])
    submit = SubmitField('Login')

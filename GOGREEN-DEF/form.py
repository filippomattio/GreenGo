from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,FileField
from wtforms.validators import DataRequired, Length,ValidationError
from app import User

class LoginForm(FlaskForm):
    username = StringField('Username:',validators=[DataRequired(),Length(min=3,max=10)])
    password = PasswordField('Password:' ,validators=[DataRequired(),Length(min=3,max=10)])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired(), Length(min=3, max=10)])
    family_name = StringField('Family name:', validators=[DataRequired(), Length(min=3, max=10)])
    username = StringField('Username:', validators=[DataRequired(), Length(min=3, max=10)])
    mail = StringField('E-Mail', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=3, max=10)])
    submit = SubmitField('Store')

    def validate_username(self, username):
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            raise ValidationError("User with name ' %s ' already exist!" % self.username.data)
import os

from flask import Flask
from flask import render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Message, Mail
from flask_bcrypt import Bcrypt
# upload image
from flask_uploads import UploadSet
from flask_uploads import configure_uploads
from flask_uploads import IMAGES, patch_request_class

# use this update to fix the  from werkzeug import secure_filename, FileStorage
# ImportError: cannot import name 'secure_filename'
# pip install -U Werkzeug==0.16.0
# set maximum file size, default is 16MB


# from form import FormContact,Registration,LogForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hard to guess'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///website_flask.db"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# EMAIL config
app.config['MAIL_USERNAME'] = os.environ['username'] #qui bisogna mettere il mio indirizzo email: ex. greengo@mail.com
app.config['MAIL_PASSWORD'] = os.environ['password']
app.config['MAIL_TLS'] = True
app.config['MAIL_SERVER'] = 'smtp.mail.com'  # bisogna registrarsi al sito mail.com!!!
app.config['MAIL_PORT'] = 587
# Upload Configuration
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + "/static"

db = SQLAlchemy(app)
# MAIL
mail = Mail(app)
bcrypt = Bcrypt(app)

# UPLOAD Then define Upload format and file size.
photos = UploadSet('photos', IMAGES)  # max 16 MB di immagini, se di piu cambiare IMAGES e mettere la size
configure_uploads(app, photos)
patch_request_class(app)

from model import User, Role
from form import RegistrationForm, LoginForm


@app.before_first_request
def create_db():
    db.drop_all()
    db.create_all()
    role_admin = Role(role_name='Admin')
    role_user = Role(role_name='User')
    role_teacher = Role(role_name='Teacher')
    pass_c = bcrypt.generate_password_hash("123456")  # per criptare la password
    user_admin = User( email="admin@admin.com", name="Mohammad", family_name="Ghazi", date_of_birth="1999/06/03",
                       password=pass_c,
                      role_name=role_admin)
    db.session.add_all([role_admin, role_user, role_teacher])
    db.session.add(user_admin)
    db.session.commit()
    # user_query = User.query.filter_by(username="admin").first()
    # print(user_query.name)


@app.route('/')
def homepage():  # put application's code here
    username = session.get('username')
    return render_template("home.html", username=username)


def send_mail(to, subject, template, **kwargs):  # to is could be a list
    msg = Message(subject, recipients=[to], sender=app.config['MAIL_USERNAME'])
    # msg.body= render_template(template + '.txt',**kwargs) solo uno dei due puo essere usato, non entrambi!
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    password = None
    email = None
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, password):
                session['email'] = email
                #session['id'] = user.id
            return redirect(url_for("welcome.html"))
        session['email'] = email
    return render_template('login.html', form=form, email=email, password=password)


@app.route('/logout', methods=['POST', 'GET'])
def logout_page():
    session.clear()
    return redirect(url_for('homepage'))


@app.route('/registration', methods=['POST', 'GET'])
def register_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        role_name = Role.query.filter_by(role_name="User").first()
        pass_c = bcrypt.generate_password_hash(form.password.data)
        new_user = User(email=form.email.data,
                        name=form.name.data,
                        family_name=form.family_name.data,
                        date_of_birth=form.date_of_birth.data,
                        password=pass_c,
                        role_name=role_name)
        #form.validate_email(form)
        db.session.add(new_user)
        db.session.commit()
        send_mail(form.email.data, "New registration", "mail", name=form.name.data, password=form.password.data,
                  email=form.email.data)
        session['email'] = form.email.data
        return redirect(url_for("welcome.html"))
    return render_template('registration.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)

import os
from datetime import datetime, date
from flask import Flask
from flask import render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Message, Mail
from flask_bcrypt import Bcrypt


# upload image
from flask_uploads import UploadSet
from flask_uploads import configure_uploads
from flask_uploads import IMAGES, patch_request_class
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
# use this update to fix the  from werkzeug import secure_filename, FileStorage
# ImportError: cannot import name 'secure_filename'
# pip install -U Werkzeug==0.16.0
# set maximum file size, default is 16MB


# from form import FormContact,Registration,LogForm

app = Flask(__name__)

app.config['GOOGLEMAPS_KEY'] = "AIzaSyDq0H2us352mUJEm1oiTuorwaZCz9ED8gU"
GoogleMaps(app)
app.config['SECRET_KEY'] = 'hard to guess'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///website_flask.db"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# EMAIL config
app.config['MAIL_USERNAME'] = "greengo2022@mail.com" #qui bisogna mettere il mio indirizzo email: ex. greengo@mail.com
app.config['MAIL_PASSWORD'] = "Greengo2022"
app.config['MAIL_TLS'] = True
app.config['MAIL_SERVER'] = 'smtp.mail.com'  # bisogna registrarsi al sito mail.com!!!
app.config['MAIL_PORT'] = 587
# Upload Configuration
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + "/static"

db = SQLAlchemy(app, session_options={"autoflush": False})
# MAIL
mail = Mail(app)
bcrypt = Bcrypt(app)

# UPLOAD Then define Upload format and file size.
photos = UploadSet('photos', IMAGES)  # max 16 MB di immagini, se di piu cambiare IMAGES e mettere la size
configure_uploads(app, photos)
patch_request_class(app)

from model import User, Role, SharingCompany, Transportation
from form import RegistrationForm, LoginForm, ChangeForm, DeleteForm, FeedbackForm


"""
@app.before_first_request
def create_db():
    db.drop_all()
    db.create_all()
    role_admin = Role(role_name='Admin')
    role_user = Role(role_name='User')
    pass_c = bcrypt.generate_password_hash("123456")  # per criptare la password
    #user_admin = User( email="admin@admin.com", name="Mohammad", family_name="Ghazi", date_of_birth="1999/06/03",
     #                  password=pass_c,
      #                role_name=role_admin)

    s1 = SharingCompany(name="Car2go", date_of_registration=date.today(),num_vehicles = 50,
                        price_per_minute = 0.26, min_age = 18, type_vehicle = "car", type_motor="electric", points="80")
    s2 = SharingCompany(name="Enjoy", date_of_registration=date.today(), num_vehicles =40,
                        price_per_minute =0.30, min_age =18, type_vehicle = "car", type_motor="hybrid", points="40")
    s3 = SharingCompany(name="Dot", date_of_registration=date.today(), num_vehicles =50,
                        price_per_minute =0.11, min_age = 16, type_vehicle = "scooter", type_motor="electric", points="90")

    db.session.add_all([role_admin, role_user])
   # db.session.add(user_admin)
    db.session.add(s1)
    db.session.add(s2)
    db.session.add(s3)
    db.session.commit()
    # user_query = User.query.filter_by(username="admin").first()
    # print(user_query.name)

"""

@app.route('/')
def homepage():  # put application's code here
    username = session.get('username')
    return render_template("home.html", username=username)

@app.route("/map")
def mapview():
    # creating a map in the view
    mymap = Map(
        identifier="view-side",
        lat=45.0578564352,
        lng=7.65664237342,
        markers=[(45.0578564352, 7.65664237342)]
    )
    sndmap = Map(

        identifier="sndmap",
        lat=45.0578564352,
        lng=7.65664237342,
        center_on_user_location=True,
        style="height:900px;width:900px;margin:4;",
        zoom=19,
        markers=[
            {
                'icon': 'https://raw.githubusercontent.com/filippomattio/flaskProject4-gogreen/main/GOGREEN-DEF/monoicon.png',
                'lat': 45.05635616,
                'lng': 7.65589579,
                'infobox': "<b>Hello World</b>"
            },
            {
                'icon': 'https://raw.githubusercontent.com/filippomattio/flaskProject4-gogreen/main/GOGREEN-DEF/monoicon.png',
                'lat': 45.05809029,
                'lng': 7.65602811,
                'infobox': "<b>Hello World</b>"
            },
            {
                'icon': 'https://raw.githubusercontent.com/filippomattio/flaskProject4-gogreen/main/GOGREEN-DEF/monoicon.png',
                'lat': 45.0578564352,
                'lng': 7.65664237342,
                'infobox': "<b>Hello World</b>"
            },
            {
                'icon': 'https://raw.githubusercontent.com/filippomattio/flaskProject4-gogreen/main/GOGREEN-DEF/monoicon.png',
                'lat': 45.0578564352,
                'lng': 7.65664237342,
                'infobox': "<b>Hello World</b>"
            },
          {
             'icon': 'https://raw.githubusercontent.com/filippomattio/flaskProject4-gogreen/main/GOGREEN-DEF/monoicon.png',
             'lat': 45.0578564352,
             'lng': 7.65664237342,
             'infobox': "<b>Hello World</b>"
          },
          {
             'icon': 'https://raw.githubusercontent.com/filippomattio/flaskProject4-gogreen/main/GOGREEN-DEF/monoicon.png',
             'lat':45.0578564352,
             'lng': 7.65664237342,
             'infobox': "<div  ><a class='link_mono' href='https://ridedott.com/it'>Dott</a></div>"
                        "<br>"
                        "<form action='https://ridedott.com/it'>"
                        "<input type='submit' class='btn btn-primary' value='Reserve now'>"
                        " </form>"
                        "<br>"
                        "<img src='https://i.etsystatic.com/17857814/r/il/7614c8/1595286099/il_fullxfull.1595286099_3t04.jpg' width='100' height='100'/>"
          }
        ]
    )
    username = session.get('username')
    return render_template('map.html', mymap=mymap, sndmap=sndmap, username=username)

def send_mail(to, subject, template, **kwargs):  # to is could be a list
    msg = Message(subject, recipients=[to], sender=app.config['MAIL_USERNAME'])
    # msg.body= render_template(template + '.txt',**kwargs) solo uno dei due puo essere usato, non entrambi!
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)


@app.route('/login3', methods=['POST', 'GET'])
def login_page():
    email = None
    password = None
    if 'email' in session:
        return redirect(url_for('confront_price'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, password):
                session['email'] = email
                return redirect(url_for('confront_price'))
            else:
                flash('Invalid password!', 'errorPassword')
        else:
            flash('Invalid email!', 'errorEmail')

    return render_template('login3.html', form=form, email=email, password=password)

@app.route('/change', methods=['POST', 'GET'])
def change():
    form = ChangeForm()
    if 'email' in session:
        email = session['email']
        if form.validate_on_submit():
            user = User.query.filter_by(email=email).first()
            if not form.validate_password(user.password, email):
                return render_template('change.html', form=form)
            db.session.delete(user)
            new_pass = form.new_password.data
            pass_c = bcrypt.generate_password_hash(new_pass)
            user.password = pass_c
            db.session.add(user)
            db.session.commit()
            flash("Password changed succesfully!", 'newPassword')
            #send_mail(email, "Change Password", "mailChange", name=user.name, password=new_pass)
            #       email=form.email.data)
            return render_template('change.html', form=form)
        return render_template('change.html', form=form)

@app.route('/logout', methods=['POST', 'GET'])
def logout_page():
    session.clear()
    return redirect(url_for('homepage'))



@app.route('/registration', methods=['POST', 'GET'])
def register_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        if not form.check_password(form.password.data) or not form.check_email(form.email.data):
            return render_template('registration.html', form=form)
        role_name = Role.query.filter_by(role_name="User").first()
        pass_c = bcrypt.generate_password_hash(form.password.data)
        new_user = User(email=form.email.data,
                        name=form.name.data,
                        family_name=form.family_name.data,
                        date_of_birth=form.date_of_birth.data,
                        password=pass_c,
                        role_name=role_name)
        if not form.validate_email(form):
            return render_template('registration.html', form=form)
        else:
            db.session.add(new_user)
            db.session.commit()
           # send_mail(form.email.data, "New registration", "mail", name=form.name.data, password=form.password.data,
            #       email=form.email.data)
            session['email'] = form.email.data
            return redirect(url_for('confront_price'))
    return render_template('registration.html', form=form)

def get_minage():
    ord = SharingCompany.query.order_by(SharingCompany.min_age).all()
    minim = ord[0].min_age
    return minim
@app.route('/reserve', methods=['POST', 'GET'])
def confront_price():
    user = User.query.filter_by(email=session['email']).first()
    today = date.today()
    age = today.year - user.date_of_birth.year
    if today.month < user.date_of_birth.month or (today.month == user.date_of_birth.month and today.day < user.date_of_birth.day):
        age -= 1
    ord = SharingCompany.query.filter(SharingCompany.min_age <= age).order_by(SharingCompany.price_per_minute).all()
    tot = len(ord)
    minim = get_minage()
    return render_template('reserve.html', ord=ord, min=minim, tot=tot)

@app.route('/settings', methods=['POST', 'GET'])
def set():
    return render_template('settings.html')
@app.route('/profile', methods=['POST', 'GET'])
def pro():
    return redirect(url_for('go', name='profile'))
@app.route('/grid', methods=['POST', 'GET'])
def pr():
    return render_template('grid.html')


@app.route('/go/<string:name>', methods=['POST', 'GET']) #tra < > bisogna mettere il nome della shar_comp in modo poi da aggiungere il transport giusto
def go(name):
    email = session['email']
    user = User.query.filter_by(email=email).first()
    if email and name != 'profile':
        tr = Transportation(user=email, sharing_company=name, date=datetime.now())
        db.session.add(tr)
        db.session.commit()
    ass = Transportation.query.filter_by(user=email).order_by(Transportation.date)
    count = 0
    points=0
    tot=0
    avg=0
    dict = {}
    for tr in ass:
        sh_co = SharingCompany.query.filter_by(name=tr.sharing_company).first()
        dict[tr.date] = sh_co
        points=points+sh_co.points
        count=count+1
        tot=tot+sh_co.price_per_minute
    if count>0:
        avg = float("{:.2f}".format(tot/count))
    return render_template('profile.html', list=ass, user=user, dict=dict, count=count, points=points, avg=avg)

@app.route('/delete', methods=['POST', 'GET'])
def delete():
    email = session['email']
    form = DeleteForm()
    user = User.query.filter_by(email=email).first()
    if user:
        if form.validate_on_submit():
            tr = Transportation.query.filter_by(user=email).all()
            for tt in tr:
                db.session.delete(tt)
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for('logout_page'))
    return render_template('delete.html', form=form, user=user)

@app.route('/feedback', methods=['POST', 'GET'])
def give_feedback():
    email = session['email']
    form = FeedbackForm()
    user = User.query.filter_by(email=email).first()
    if email:
        if form.validate_on_submit():
            #devo aggiungere il feedback al database
            return render_template('reserve.html')
    return render_template('feedback.html', form=form, user=user)

@app.route('/footers', methods=['POST', 'GET'])
def foot():
    return render_template('footers.html')
if __name__ == '__main__':
    app.run(debug=True)

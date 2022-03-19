import os
from datetime import datetime, date, time, timedelta
from time import strptime, strftime

from flask import Flask, make_response, request
from flask import render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_mail import Message, Mail
import socket
import geocoder
from flask_bcrypt import Bcrypt
from random import randint, random, uniform

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
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

app.config['GOOGLEMAPS_KEY'] = "AIzaSyDq0H2us352mUJEm1oiTuorwaZCz9ED8gU"
GoogleMaps(app)
app.config['SECRET_KEY'] = 'hard to guess'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///website_flask.db"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# EMAIL config
app.config[
    'MAIL_USERNAME'] = 'greengo2022@email.com'  # qui bisogna mettere il mio indirizzo email: ex. greengo@mail.com
app.config['MAIL_PASSWORD'] = 'Greengo2022'
app.config['MAIL_TLS'] = True
app.config['MAIL_SERVER'] = 'smtp.mail.com'  # bisogna registrarsi al sito mail.com!!!
app.config['MAIL_PORT'] = 25
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

from flag import Flag
from model import User, SharingCompany, Transportation, Rating, FinalFeedback, Mean, Prize
from form import RegistrationForm, LoginForm, ChangeForm, DeleteForm, FeedbackForm, RecoverForm, ReservateForm, Delete, \
    Unlock, SelectMean, PrizeForm

flag = Flag()
flag2 = Flag()

"""
@app.before_first_request
def create_db():
    db.drop_all()
    db.create_all()
    s1 = SharingCompany(name="Car2go", date_of_registration=date.today(),num_vehicles = 50,
                        price_per_minute = 0.26, min_age = 18, type_vehicle = "car", type_motor="electric", points="80", reservation_time=time(minute=15))
    s2 = SharingCompany(name="Enjoy", date_of_registration=date.today(), num_vehicles =40,
                        price_per_minute =0.30, min_age =18, type_vehicle = "car", type_motor="hybrid", points="40", reservation_time=time(minute=15))
    s3 = SharingCompany(name="Dot", date_of_registration=date.today(), num_vehicles =50,
                        price_per_minute =0.11, min_age = 16, type_vehicle = "scooter", type_motor="electric", points="90", reservation_time=time(minute=15))
    for i in range(400):
        id=str(i)
        lat=uniform(45.039541, 45.095419)
        lng=uniform(7.634643, 7.688886)
        m1 = Mean(id=id, sharing_company="Dot", lat=lat, lng=lng)
        db.session.add(m1)
    for i in range(400):
        id=str(i)
        lat=uniform(45.039541, 45.095419)
        lng=uniform(7.634643, 7.688886)
        m1 = Mean(id=id, sharing_company="Enjoy", lat=lat, lng=lng)
        db.session.add(m1)
    db.session.add(s1)
    db.session.add(s2)
    db.session.add(s3)
    p1 = Prize(name="Travel", company="Rainair", points=40)
    p2 = Prize(name="Travel", company="Lufthansa", points=10)
    db.session.add(p1)
    db.session.add(p2)
    db.session.commit()

"""


@app.route("/cookie/<string:name>/<string:id>/<string:email>/<int:seconds>", methods=['GET', 'POST'])
def setcookie(name, id, email, seconds):
    resp = make_response(redirect(url_for('reservation', id=id, name=name)))
    now = datetime.now()
    value = now + timedelta(seconds=seconds)
    value = value.strftime("%Y/%m/%d %H:%M:%S")
    resp.set_cookie(email, value, max_age=seconds)
    return resp


@app.route('/')
def homepage():
    username = session.get('username')
    tot = Rating.query.all()
    count = 0
    rating = 0
    avg = 0
    for rt in tot:
        rating = rating + rt.rank
        count = count + 1
    if count > 0:
        avg = float("{:.2f}".format(float(rating) / float(count)))
    avg_int = int(avg)
    return render_template("home.html", username=username, rating=avg, count=count, avg_int=avg_int)


@app.route("/map/<string:name>", methods=['GET', 'POST'])
def mapview(name):
    # creating a map in the view
    if 'email' not in session or session['email'] in request.cookies:
        redirect(url_for('homepage'))
    g = geocoder.ipinfo('me')
    latlng = g.latlng
    latUser = latlng[0]
    lngUser = latlng[1]
    sndmap = Map(

        identifier="sndmap",
        lat=45.0578564352,
        lng=7.65664237342,
        center_on_user_location=True,
        style="height:500px;width:100%;margin:4;",
        zoom=19,
        markers=[
            {
                'icon': 'https://raw.githubusercontent.com/filippomattio/flaskProject4-gogreen/main/GOGREEN-DEF/symbol_blank.png',
                'lat': latUser,
                'lng': lngUser,

            }
        ]
    )
    means = Mean.query.filter_by(sharing_company=name)
    for m in means:
        if m.sharing_company == 'Dot':
            new_marker = {
                'icon': 'https://raw.githubusercontent.com/filippomattio/flaskProject4-gogreen/main/GOGREEN-DEF/monoicon.png',
                'lat': m.lat,
                'lng': m.lng,
                'infobox': "<div  ><a class='link_mono' href='https://ridedott.com/it'>Dot</a></div>"
                           "<br>"
                           "<form action='/go/Dot/" + str(m.id) + "'>"
                                                                  "<input type='submit' class='btn btn-primary' value='Reserve now'>"
                                                                  " </form>"
                                                                  "<br>"
                                                                  "<img src='https://i.etsystatic.com/17857814/r/il/7614c8/1595286099/il_fullxfull.1595286099_3t04.jpg' width='100' height='100'/>"
            }
        if m.sharing_company == 'Enjoy':
            new_marker = {
                'icon': 'https://raw.githubusercontent.com/filippomattio/flaskProject4-gogreen/main/GOGREEN-DEF/car.png',
                'lat': m.lat,
                'lng': m.lng,
                'infobox': "<div  ><a class='link_mono' href='https://enjoy.eni.com/it'>Enjoy</a></div>"
                           "<br>"
                           "<form action='/go/Enjoy/" + str(m.id) + "'>"
                                                                    "<input type='submit' class='btn btn-primary' value='Reserve now'>"
                                                                    " </form>"
                                                                    "<br>"
                                                                    "<img src='data:image/png;base64,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' width='100' height='100'/>"
            }
        sndmap.markers.append(new_marker)
    user = User.query.filter_by(email=session['email']).first()
    username = user.name
    class_temp = "container px-4 py-5 mt-4"
    return render_template('map.html', sndmap=sndmap, username=username, class_temp=class_temp)


@app.route("/map", methods=['GET', 'POST'])
def mapview2():
    # creating a map in the view
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        name = user.name
        if user:
            today = date.today()
            age = today.year - user.date_of_birth.year
            if today.month < user.date_of_birth.month or (
                    today.month == user.date_of_birth.month and today.day < user.date_of_birth.day):
                age -= 1
        else:
            age = 99
    else:
        age = 99
        name = "new user"
    g = geocoder.ipinfo('me')
    latlng = g.latlng
    latUser = latlng[0]
    lngUser = latlng[1]

    sndmap = Map(

        identifier="sndmap",
        lat=45.0578564352,
        lng=7.65664237342,
        center_on_user_location=True,
        style="height:500px;width:100%;margin:4;",
        zoom=19,

        markers=[
            {
                'icon': 'https://raw.githubusercontent.com/filippomattio/flaskProject4-gogreen/main/GOGREEN-DEF/symbol_blank.png',
                'lat': latUser,
                'lng': lngUser,

            }
        ]
    )
    means = Mean.query.all()
    for m in means:
        sh_co = SharingCompany.query.filter_by(name=m.sharing_company).first()
        if m.sharing_company == 'Dot' and sh_co.min_age <= age:
            new_marker = {
                'icon': 'https://raw.githubusercontent.com/filippomattio/flaskProject4-gogreen/main/GOGREEN-DEF/monoicon.png',
                'lat': m.lat,
                'lng': m.lng,
                'infobox': "<div  ><a class='link_mono' href='https://ridedott.com/it'>Dott</a></div>"
                           "<br>"
                           "<form action='/go/" + str(m.sharing_company) + "/" + str(m.id) + "'>"
                                                                                             "<input type='submit' class='btn btn-primary' value='Reserve now'>"
                                                                                             " </form>"
                                                                                             "<br>"
                                                                                             "<img src='https://i.etsystatic.com/17857814/r/il/7614c8/1595286099/il_fullxfull.1595286099_3t04.jpg' width='100' height='100'/>"
            }
        if m.sharing_company == 'Enjoy' and sh_co.min_age <= age:
            new_marker = {
                'icon': 'https://raw.githubusercontent.com/filippomattio/flaskProject4-gogreen/main/GOGREEN-DEF/car.png',
                'lat': m.lat,
                'lng': m.lng,
                'infobox': "<div  ><a class='link_mono' href='https://enjoy.eni.com/it'>Enjoy</a></div>"
                           "<br>"
                           "<form action='/go/" + str(m.sharing_company) + "/" + str(m.id) + "'>"
                                                                                             "<input type='submit' class='btn btn-primary' value='Reserve now'>"
                                                                                             " </form>"
                                                                                             "<br>"
                                                                                             "<img src='data:image/png;base64,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' width='100' height='100'/>"
            }
        sndmap.markers.append(new_marker)
    username = session.get('username')
    class_temp = "container px-4 py-4"
    return render_template('map.html', sndmap=sndmap, username=name, class_temp=class_temp)


def send_mail(to, subject, template, **kwargs):  # to is could be a list
    msg = Message(subject, recipients=[to], sender=app.config['MAIL_USERNAME'])
    # msg.body= render_template(template + '.txt',**kwargs) solo uno dei due puo essere usato, non entrambi!
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)


@app.route("/reservation/<string:name>/<string:id>", methods=['GET', 'POST'])
def reservation(name, id):
    cookie = request.cookies.get(session['email'])
    if 'email' not in session or not cookie:
        return redirect(url_for('homepage'))
    email = session['email']
    user = User.query.filter_by(email=email).first()
    form1 = Delete()
    form2 = Unlock()
    if form1.submit1.data and form1.validate():
        tt = Transportation.query.filter_by().order_by(desc(Transportation.date)).first() #a cosa serve?
        session['delete'] = 'clear'
        flag.SetFlag(True)
        resp = make_response(redirect(url_for('pro')))
        resp.set_cookie(email, cookie, max_age=0)
        return resp
    if form2.submit2.data and form2.validate():
        tt = Transportation.query.filter_by().order_by(desc(Transportation.date)).first() #a cosa serve?
        session['unlock'] = 'unlock'
        flag.SetFlag(False)
        resp = make_response(redirect(url_for('pro')))
        resp.set_cookie(email, cookie, max_age=0)
        return resp
    id = int(id)
    g = geocoder.ipinfo('me')
    latlng = g.latlng
    latUser = latlng[0]
    lngUser = latlng[1]
    sndmap = Map(

        identifier="sndmap",
        lat=45.0578564352,
        lng=7.65664237342,
        center_on_user_location=True,
        style="height:500px;width:100%;margin:4;",
        zoom=19,
        markers=[
            {
                'icon': 'https://raw.githubusercontent.com/filippomattio/flaskProject4-gogreen/main/GOGREEN-DEF/symbol_blank.png',
                'lat': latUser,
                'lng': lngUser,
            }
        ]
    )
    m = Mean.query.filter_by(sharing_company=name, id=id).first()

    if name == 'Dot':
        new_marker = {
            'icon': 'https://raw.githubusercontent.com/filippomattio/flaskProject4-gogreen/main/GOGREEN-DEF/monoicon.png',
            'lat': m.lat,
            'lng': m.lng,
            'infobox': "<div  ><a class='link_mono' href='https://ridedott.com/it'>Dot</a></div>"
                       "<br>"

                       "<br>"
                       "<img src='https://i.etsystatic.com/17857814/r/il/7614c8/1595286099/il_fullxfull.1595286099_3t04.jpg' width='100' height='100'/>"
        }
    if m.sharing_company == 'Enjoy':
        new_marker = {
            'icon': 'https://raw.githubusercontent.com/filippomattio/flaskProject4-gogreen/main/GOGREEN-DEF/car.png',
            'lat': m.lat,
            'lng': m.lng,
            'infobox': "<div  ><a class='link_mono' href='https://enjoy.eni.com/it'>Enjoy</a></div>"
                       "<br>"

                       "<br>"
                       "<img src='data:image/png;base64,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' width='100' height='100'/>"
        }
    sndmap.markers.append(new_marker)
    username = session.get('username')

    now = datetime.now()
    end = datetime.strptime(cookie, "%Y/%m/%d %H:%M:%S")
    time = (end - now)
    time = str(time).split(".")[0]
    email = session['email']
    ass = Transportation.query.filter_by().order_by(desc(Transportation.date)).first

    return render_template('reservation.html', user=user, sndmap=sndmap, username=username, time=time, ass=ass,
                           form1=form1, form2=form2)


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
            flash("Password changed successfully!", 'newPassword')
            send_mail(email, "Change Password", "mailChange", name=user.name, password=new_pass)
            return render_template('change.html', form=form)
        return render_template('change.html', form=form)
    return redirect(url_for('homepage'))


@app.route('/logout', methods=['POST', 'GET'])
def logout_page():
    session.clear()
    return redirect(url_for('homepage'))


@app.route('/registration', methods=['POST', 'GET'])
def register_page():
    if 'email' in session:
        return redirect(url_for('login_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if not form.check_password(form.password.data) or not form.check_email(form.email.data):
            return render_template('registration.html', form=form)
        if not form.validate_email(form):
            return render_template('registration.html', form=form)
        else:
            pass_c = bcrypt.generate_password_hash(form.password.data)
            new_user = User(email=form.email.data,
                            name=form.name.data,
                            family_name=form.family_name.data,
                            date_of_birth=form.date_of_birth.data,
                            password=pass_c)
            try:
                send_mail(form.email.data, "New registration", "mail", user=new_user, password=form.password.data)
            except:
                flash("Email not valid. Please retry with a new one.", 'errorEmail')
                return render_template('registration.html', form=form)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = form.email.data
            return redirect(url_for('confront_price'))
    return render_template('registration.html', form=form)


def get_minage():
    ord = SharingCompany.query.order_by(SharingCompany.min_age).all()
    minim = ord[0].min_age
    return minim


@app.route('/reserve', methods=['POST', 'GET'])
def confront_price():
    if 'email' not in session:
        return redirect(url_for('login_page'))
    user = User.query.filter_by(email=session['email']).first()
    today = date.today()
    age = today.year - user.date_of_birth.year
    if today.month < user.date_of_birth.month or (
            today.month == user.date_of_birth.month and today.day < user.date_of_birth.day):
        age -= 1
    form2 = SelectMean()
    flag = True
    flagAll = True

    if form2.submit2.data and form2.validate():
        if form2.select.data == 'all':
            flagAll = False
            ord = SharingCompany.query.filter(SharingCompany.min_age <= age
                                              ).order_by(
                SharingCompany.price_per_minute).all()

        if flagAll == True and len(SharingCompany.query.filter(SharingCompany.min_age <= age,
                                                               SharingCompany.type_vehicle == form2.select.data).all()) == 0:
            flag = False
        if flag and flagAll == True:
            ord = SharingCompany.query.filter(SharingCompany.min_age <= age,
                                              SharingCompany.type_vehicle == form2.select.data).order_by(
                SharingCompany.price_per_minute).all()
        if flag == False and flagAll == True:
            ord = []


    else:
        ord = SharingCompany.query.filter(SharingCompany.min_age <= age).order_by(SharingCompany.price_per_minute).all()
    tot = len(ord)
    minim = get_minage()
    form = ReservateForm()
    if form.submit.data and form.validate():
        return redirect(url_for('mapview'))
    if user.email in request.cookies and 'unlock' in session:
        ass = Transportation.query.filter_by(user=user.email).order_by(desc(Transportation.date)).all()
        st = session['unlock']
        tt = st.split(",")

        id = int(tt[3])
        sh_co = tt[1]
        # id = ass[0].id
        # sh_co = ass[0].sharing_company
        return render_template('reserve.html', ord=ord, min=minim, tot=tot, form=form, user=user, sh_co=sh_co, id=id,
                               form2=form2, flag=flag)
    if user.email in request.cookies and 'unlock' not in session and flag2.getFlag():
        return render_template('reserve.html', ord=ord, min=minim, tot=tot, form=form, user=user, sh_co=session['sc_first'] , id=session['id_first'],
                               form2=form2, flag=flag)

    if form2.submit2.data and form2.validate():
        return render_template('reserve.html', ord=ord, min=minim, tot=tot, form=form, user=user,
                               form2=form2, flag=flag)

    return render_template('reserve.html', ord=ord, min=minim, tot=tot, form=form, user=user, form2=form2, flag=flag)


@app.route('/prize', methods=['POST', 'GET'])
def prize():
    if 'email' not in session:
        points=0
        flag = False
    else:
        user = User.query.filter_by(email=session['email']).first()
        points=user.points
        flag = True
    form = PrizeForm()
    ord = Prize.query.filter_by().order_by(Prize.points).all()
    return render_template('prize.html', ord=ord, form=form, points=points, flag=flag)


@app.route('/prize/<string:name>/<string:company>', methods=['POST', 'GET'])
def prize2(name, company):
    if 'email' not in session:
        return redirect(url_for('login_page'))
    user = User.query.filter_by(email=session['email']).first()
    form = PrizeForm()
    flag = True
    ord = Prize.query.filter_by(company=company, name=name).order_by(desc(Prize.points)).first()
    user.points = user.points - ord.points
    try:
        send_mail(session['email'], "Coupon bought", "mailPrize", points=user.points, company=company, name_coupon=name,
                  name_user=user.name)
    except:
        return redirect(url_for('homepage'))
    return redirect(url_for('homepage'))


@app.route('/settings', methods=['POST', 'GET'])
def set():
    return render_template('settings.html')
@app.route('/aboutus', methods=['POST', 'GET'])
def aboutus():
    return render_template('aboutus.html')

@app.route('/profile', methods=['POST', 'GET'])
def pro():
    return redirect(url_for('go', name='profile', id=0))


@app.route('/recover', methods=['POST', 'GET'])
def recover_page():
    form = RecoverForm()
    if form.validate_on_submit():
        if not form.check_email(form):
            render_template("recover.html", form=form)
        else:
            user = User.query.filter_by(email=form.email.data).first()
            new_pass = user.name[0:2] + user.family_name[0:2] + str(randint(1000, 100000000000))
            pass_c = bcrypt.generate_password_hash(new_pass)
            user.password = pass_c
            send_mail(user.email, "New Password", "mailRecover", user=user, password=new_pass)
            return render_template("recover.html", form=form)
    return render_template("recover.html", form=form)


@app.route('/go/<string:name>/<string:id>', methods=['POST',
                                                     'GET'])
def go(name, id):
    if 'email' not in session:
        return redirect(url_for('login_page'))
    email = session['email']
    user = User.query.filter_by(email=email).first()
    if user.email in request.cookies and name != 'profile' and 'unlock' in session:
        tot_tr = Transportation.query.filter_by(user=email).order_by(desc(Transportation.date)).all()
        st = session['unlock']
        tt = st.split(",")
        id = int(tt[3])
        sh_co = tt[1]
        return redirect(url_for('reservation', name=sh_co, id=id))
    if email and name != 'profile':
        tr = Transportation(user=email, sharing_company=name, date=datetime.now(), id=id)
        sh = SharingCompany.query.filter_by(name=tr.sharing_company).first()
        reservation_time = sh.reservation_time
        seconds = sh.reservation_time.hour * 3600 + sh.reservation_time.minute * 60 + sh.reservation_time.second
        db.session.add(tr)
        db.session.commit()
        flag2.SetFlag(False)
        if 'unlock' in session:
             session['unlock'] = tr.user + "," + tr.sharing_company + "," + str(tr.date) + "," + str(tr.id)
        send_mail(email, "Greengo Reservation", "mailReserve", user=user, transportation=tr,
                  reservation_time=reservation_time)
        return redirect(url_for('setcookie', id=id, name=name, email=email, seconds=seconds))
    if 'unlock' not in session and user.email in request.cookies and flag2.getFlag() == False:
        tr = Transportation.query.filter_by(user=session['email']).order_by(desc(Transportation.date)).first()
        id_reservation = tr.id
        name_reservation = tr.sharing_company
        session['id_first']=tr.id
        session['sc_first'] = tr.sharing_company
        flag2.SetFlag(True)
        db.session.delete(tr)
        db.session.commit()
    else:
        id_reservation = ""
        name_reservation = ""
    ass = Transportation.query.filter_by(user=session['email']).order_by(desc(Transportation.date)).all()
    count = 0
    points = 0
    tot = 0
    avg = 0
    dict = {}
    if len(ass) > 0:
        for tr in ass:
            sh_co = SharingCompany.query.filter_by(name=tr.sharing_company).first()
            dict[tr.date] = sh_co
            count = count + 1
            tot = tot + sh_co.price_per_minute
        id_reservation = ass[0].id
        name_reservation = ass[0].sharing_company
        to_delete = ass[0]
    if 'unlock' in session:
        if flag2.getFlag() == True:
            st = session['unlock']
            tt = st.split(",")
            tr = Transportation(tt[0], tt[1], datetime.strptime(tt[2], '%Y-%m-%d %H:%M:%S.%f'), int(tt[3]))
            db.session.add(tr)
            db.session.commit()
        tr = Transportation.query.filter_by(user=session['email']).order_by(desc(Transportation.date)).first()
        sh_co = SharingCompany.query.filter_by(name=tr.sharing_company).first()
        user.points = user.points + sh_co.points
        session.pop('unlock', None)
    if 'delete' in session and flag.getFlag() == False:
        session['delete'] = ''
    if 'delete' in session and flag.getFlag() == True:
        flag.SetFlag(False)
    if count > 0:
        avg = float("{:.2f}".format(tot / count))
    return render_template('profile.html', list=ass, user=user, dict=dict, count=count, points=user.points, avg=avg,
                           id_reservation=id_reservation, name_reservation=name_reservation, session2=True)


@app.route('/delete', methods=['POST', 'GET'])
def delete():
    email = session['email']
    form = DeleteForm()
    user = User.query.filter_by(email=email).first()

    if user:
        if form.validate_on_submit():
            ff = FinalFeedback(user=email, motivation=form.motivation.data, other=form.other.data)
            tr = Transportation.query.filter_by(user=email).all()
            for tt in tr:
                db.session.delete(tt)
            db.session.add(ff)
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for('logout_page'))
    return render_template('delete.html', form=form, user=user)


@app.route('/feedback', methods=['POST', 'GET'])
def give_feedback():
    email = session['email']
    if 'email' not in session:
        redirect(url_for('homepage'))
    form = FeedbackForm()
    user = User.query.filter_by(email=email).first()
    if email:
        if form.validate_on_submit():
            rating = Rating(user=email, rank=form.rank.data, date=datetime.now(), reason=form.reason.data)
            db.session.add(rating)
            db.session.commit()
            return redirect(url_for('homepage'))
    return render_template('feedback.html', form=form, user=user)


@app.route('/footers', methods=['POST', 'GET'])
def foot():
    return render_template('footers.html')


if __name__ == '__main__':
    app.run(debug=True)

@app.errorhandler(404)
def error404(error):
    return render_template('404.html'), 404
@app.errorhandler(403)
def error403(error):
    return render_template('403.html'), 403
@app.errorhandler(500)
def error500(error):
    return render_template('500.html'), 500
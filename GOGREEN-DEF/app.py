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
    'MAIL_USERNAME'] = 'greengoo@mail.com'  # qui bisogna mettere il mio indirizzo email: ex. greengo@mail.com
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
    s4 = SharingCompany(name="Mobike", date_of_registration=date.today(), num_vehicles =60,
                        price_per_minute =0.07, min_age = 17, type_vehicle = "bike", type_motor="none", points="150", reservation_time=time(minute=15))
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
    for i in range(400):
        id=str(i)
        lat=uniform(45.039541, 45.095419)
        lng=uniform(7.634643, 7.688886)
        m1 = Mean(id=id, sharing_company="Car2go", lat=lat, lng=lng)
        db.session.add(m1)
    for i in range(400):
        id=str(i)
        lat=uniform(45.039541, 45.095419)
        lng=uniform(7.634643, 7.688886)
        m1 = Mean(id=id, sharing_company="Mobike", lat=lat, lng=lng)
        rating = Rating(user="greengoo@mail.com", rank=randint(3,5), date=datetime.now(), reason="")
        db.session.add(rating)
        db.session.add(m1)        
    db.session.add(s1)
    db.session.add(s2)
    db.session.add(s3)
    db.session.add(s4)
    p1 = Prize(name="Travel", company="GreenTravel", points=40)
    p2 = Prize(name="Food", company="VeganVibes", points=10)
    db.session.add(p1)
    db.session.add(p2)
    db.session.commit()



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

    sndmap = Map(

        identifier="sndmap",
        lat=45.0578564352,
        lng=7.65664237342,
        center_on_user_location=True,
        style="height:500px;width:100%;margin:4;",
        zoom=19,
        markers=[
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
                                                                  "<img src='data:image/jpeg;base64,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' width='100' height='100'/>"
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
        if m.sharing_company == 'Car2go':
            new_marker = {
                'icon': 'https://raw.githubusercontent.com/filippomattio/flaskProject4-gogreen/main/GOGREEN-DEF/sportutilityvehicle.png',
                'lat': m.lat,
                'lng': m.lng,
                'infobox': "<div  ><a class='link_mono' href='https://www.share-now.com/it/it/turin/'>Car2go</a></div>"
                           "<br>"
                           "<form action='/go/Car2go/" + str(m.id) + "'>"
                                                                    "<input type='submit' class='btn btn-primary' value='Reserve now'>"
                                                                    " </form>"
                                                                    "<br>"
                                                                    "<img src='data:image/png;base64,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' width='100' height='100'/>"
            }
        if m.sharing_company == 'Mobike':
            new_marker = {
                'icon': 'https://raw.githubusercontent.com/filippomattio/flaskProject4-gogreen/main/GOGREEN-DEF/cycling.png',
                'lat': m.lat,
                'lng': m.lng,
                'infobox': "<div  ><a class='link_mono' href='https://it-it.facebook.com/MobikeIT/'>Mobike</a></div>"
                           "<br>"
                           "<form action='/go/Mobike/" + str(m.id) + "'>"
                                                                    "<input type='submit' class='btn btn-primary' value='Reserve now'>"
                                                                    " </form>"
                                                                    "<br>"
                                                                    "<img src='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAkFBMVEX/RhH/////VSj/Qwr/ZkL/QAD/OAD/MwD/MQD/OgD/5N7/gGb/Qgb/4dv/Yzz/TB7/wbb/uaz/jnj/sqT/2tL/7ur/+vn/0cj/8u//eV7/vbH/Sxf/h3D/ppb/noz/y8D/bEz/zcT/lH//hW3/q5v/Xjf/dFf/mof/e2H/dFn/cU//jXb/aEj/WC7/qpr/IQBjqV7LAAAJBUlEQVR4nO2ca3fqKhCGjRRIrLZar7VVq/be2vP//92JJlySACaQRGcv3g9n7Spn5HFgYGBip9v5t9XteELo8oTw5QnhyxPClyeEL08IX54QvjwhfHlC+PKE8OUJ4csTwpcnhC9PCF+eEL48IXx5QvjyhPDlCeHLE8KXJ4QvTwhfnhC+PCF8eUL48oTw5QnhyxPClyeEL08IX54QvjwhfF0TYUQpiTCq2eoVEZLNtDcfPXRDgus0e0WEdBKcNB39hjUyXiFhrN4PrY3xOgljR36FNU3IayUMgg2ux43XSxjMXkgdZlsnxBHhijLv5AmD4IfW8IEtE6JwPx5xjTOIdJAnDNah+0e2S4jup1knZRAJ6e7HWcwP94HaLmGYG4iLHADCUdgdz6QWn5HaUnm1Soi6+WH4UQRABI+lFt2+44e2Sohf8oQz1ShE9GbBW/Rco027hL+FWPKqnGg4EsN57ThOL00YyLmE+CeSZmzHbXNz4VEaBCPhxPunkDKHIdpjLZZu8bTlSLN7SPXMl40ucxHZBMHkA6eM/Xulm6ur5fUQM5Fn1v8NCyVkeIo9u/Tv6IG1WDnNxIvtS0M+Ct/S9SAhDII5QdkWU6dwejFC/MgI5+nWjBEGA5prceeyJl4utxDR8iVJkzhhMEwQQzZXnYbp5QjF0jFInCgIg/cTc/THvOwyTGskRBFVS3OyRLcM6PPUQCJMxmn/Jv1z4ZJi1EeIO6NBT6nto3JFE7vUJJRIhOnMI2wP/uSwXtRGiLpySpDTWolIOdLDcaLJhMnM4xnjr0OoqY2wmKHL6qqcgPiivjg6USbcnr4Swsbxu8ORTV2EqGMC1GyfyVh+/7inYeplx+3zNRAWUr+M/pSECLORPYvfR4c7rreTz9krN/cOPWuJUDPMohVrcMyiUJ8rHdTsFZeetUM40YV7Hi1dcyS9WiHU5z/Rjrep4+RQpfrWw3shPGL9vj2+jA0JHt+ZBYeGnFgfIRLCT6zbgzD+0/R/4T1rumnIic3sSwl34uO5OF/MompWM4RIcuKZpvj9bDhyU0O5hXDi11knzllTl52LXg0RVnBiOCjd1EpN5YelZyK+FavKvgknNkWIUEnPiEgTZ1FNOLGxHL+kE2UXBsHO+R6mqMYIS85E2YXxBryBNbG5c5pSTsy60PVoVKnmCEV+a3Bi1oWxE2sviWryrE04UbvQ5V0YBONaqhNkNUgo0n6tE7kLZ3wDfg+pru3sTBQufOXXGMO6g02ThGfDqZiFOCzeRdWkRs+8zzhRuHBMxL+3NTuxBkKEIxrSKP4PibIgZ5woXBjnkGJ7+ovxyVZEYqvusdWZEFO8H8+ns1jT+fgWZ4oKjSmG7EL5fnhC9+NJYnAy2iPXKkVHwih85slPovmtVBxqdKJw4eloLV9rw4Gfw8vdkOJwtyh2afEgGA0zMevCTqf/piY8Xgu7VNS6EJLfqbpLvTu2bhtSDCmQJnONbtTWYk1v7DcCDoThn7ZHouRO68S8C2Mnmi4GVtaJlTUhonNDh4JN2iPtTMwE0lPLUO/DWFvbmmFbQkSKtZIZ8dt5tRMLLjxrcEDsEG0JC5dps/z14TZB1KQYwoXpcX5hSBQMWt51WxKGS/mzh88HEobR209mnL0mPVKmGAUXhuOiQXJ4Hsqvjqzmoh1h9Cw+d7amJImGCBOyknqUDEtlipEPpHIalTFI15Irb20WDStCce93LKnP1vl2xGhL62MVMzHvQtngtp8xGOGtYLdZ+q0IiRijq3yIQ9J4S0orFeE070LxJQR/RYNiXIwslkUbQukm7UMxNaR1Mt//1IkFF4oqPVXtevjB37YoyrAhFD1Wz/2Qx4fX07AqODG/FgqDS7VBPmYsnGhDGLFJozvBpWy3WpiJpxSjEEiFQc2CwPNji5loQSg6qDthEpeCSYucE3NJhWRQd+4oivg+K4dTC0JRQ6hdnzhD+sxIZiYWXFjGINvwVC8YtiDkQ+ZH+31GLDYM/ksfAArEC//lkwpucKc1iFk5bfWrDZtRyjqoL58Q0XY5PGnJ86zNcJtzoTCoj5RinLcwSvlxQ8/wdYaazDGjNKnoszJMk3/4uK9c4mZByKbRxjAliDG1yrnwM31hazLItryVQ40F4Q/roSFyk6ECKSc2yDHb5JoWOx6r9JNfo6YIxwoktQvLEUbMYJuExq/cmK+fxE9COaFpJeBb4cplihaEZaaNudo040KxnJtSXJ4gny3Qyas6Yf8u/SxT6KOGguGcC8UxoqmcO2Qbwbeqe2+bPQ3rpP4OhX8Ls/dbtV6wwqC+tA0dWJtW9jRsadJfSfNAMwmxRlJrXs6tN8gLUQeVD2ssCHlY048qPkhL3cuXMMgHqSmAq2Wza/tmI0ZXHELWrEWpajxxKaN4aPYkvs8NXtrILTqUb8nUd1/iwbqSj7gKg+qtrrgbsKgpssqAuYsmKgJEePJQsgJIGBxQFaK4W7R4ZNbqJIrn5MGmeNaORLFh/mF0rUS591xlcMvetTlssyPk33kwzz/UJD+k/FC2Q2KeBZOCQSIM6uapSXYnwlJytPiSL/dw+CnW+grVlFLl0OIxa/BLenLd5tDbjhDfBULzd0owRghHhD7Ku7UKVRWZ69HJ++n3ohDGhL7LaZhVnbTlvQV5kD44mA53X4fD126YuRHeVxlS0Y/SYCaR/rG67ba+ezJcjyZaV9t90NU5g6tW757yl0WK/lSdM6Yr5aNeLW+B7W+5w7WpP7vq/aEfJoOq+4NScrjHJ9/aFGnxa1NZQF4UlR2pQftfVHKpxcBkqe7P2LLKB0t3UBktHX6kzq1iiL4pTiuGXfvSEHJQGNy8XfBZ7j69X2UqDCbrjmVFATP4tM4YHKyf6GWfP0RRGH2ulpvJZLNcPxIauZbaoYhyg6vP2LqjwVqqL4+/UEYpyZcmXofBK/pFuobkCeHLE8KXJ4QvTwhfnhC+PCF8eUL48oTw5QnhyxPClyeEL08IX54QvjwhfHlC+PKE8OUJ4csTwpcnhC9PCF+eEL48IXx5QvjyhPDlCeHLE8KXJ4QvTwhfnhC+PCF8eUL4ign76F9Wv9v5vvm39f0/Pu9yk7cMc4QAAAAASUVORK5CYII=' width='100' height='100'/>"
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


    sndmap = Map(

        identifier="sndmap",
        lat=45.0578564352,
        lng=7.65664237342,
        center_on_user_location=True,
        style="height:500px;width:100%;margin:4;",
        zoom=19,

        markers=[

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
                                                                                             "<img src='data:image/jpeg;base64,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' width='100' height='100'/>"
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
                                                                                             "<img src='https://www.trenitalia.com/content/dam/tcom/immagini/trenitalia-img/offerte-e-servizi/servizi/416x359/416x359-Enjoy-ENI-CarSharing.jpg' width='100' height='100'/>"
            }
        if m.sharing_company == 'Car2go' and sh_co.min_age <= age:
            new_marker = {
                'icon': 'https://raw.githubusercontent.com/filippomattio/flaskProject4-gogreen/main/GOGREEN-DEF/sportutilityvehicle.png',
                'lat': m.lat,
                'lng': m.lng,
                'infobox': "<div  ><a class='link_mono' href='https://www.share-now.com/it/it/turin/'>Car2go</a></div>"
                           "<br>"
                           "<form action='/go/Car2go/" + str(m.id) + "'>"
                                                                    "<input type='submit' class='btn btn-primary' value='Reserve now'>"
                                                                    " </form>"
                                                                    "<br>"
                                                                    "<img src='https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Car2go_logo.svg/1200px-Car2go_logo.svg.png' width='100' height='100'/>"
            }
        if m.sharing_company == 'Mobike' and sh_co.min_age <= age:
            new_marker = {
                'icon': 'https://raw.githubusercontent.com/filippomattio/flaskProject4-gogreen/main/GOGREEN-DEF/cycling.png',
                'lat': m.lat,
                'lng': m.lng,
                'infobox': "<div  ><a class='link_mono' href='https://it-it.facebook.com/MobikeIT/'>Mobike</a></div>"
                           "<br>"
                           "<form action='/go/Mobike/" + str(m.id) + "'>"
                                                                    "<input type='submit' class='btn btn-primary' value='Reserve now'>"
                                                                    " </form>"
                                                                    "<br>"
                                                                    "<img src='data:image/png;base64,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' width='100' height='100'/>"
            }
        sndmap.markers.append(new_marker)
    username = session.get('username')
    class_temp = "container px-4 py-4"
    return render_template('map.html', sndmap=sndmap, username=name, class_temp=class_temp)


def send_mail(to, subject, template, **kwargs):
    msg = Message(subject, recipients=[to], sender=app.config['MAIL_USERNAME'])
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
    session['unlock'] = name+","+str(id)
    if form1.submit1.data and form1.validate():
        tt = Transportation.query.filter_by().order_by(desc(Transportation.date)).first()
        session['delete'] = 'clear'
        flag.SetFlag(True)

        resp = make_response(redirect(url_for('pro')))
        resp.set_cookie(email, cookie, max_age=0)
        return resp
    if form2.submit2.data and form2.validate():
        tt = Transportation.query.filter_by().order_by(desc(Transportation.date)).first()
        session['validate'] = 'unlock'
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
                       "<img src='data:image/jpeg;base64,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' width='100' height='100'/>"
        }
    if m.sharing_company == 'Enjoy':
        new_marker = {
            'icon': 'https://raw.githubusercontent.com/filippomattio/flaskProject4-gogreen/main/GOGREEN-DEF/car.png',
            'lat': m.lat,
            'lng': m.lng,
            'infobox': "<div  ><a class='link_mono' href='https://enjoy.eni.com/it'>Enjoy</a></div>"
                       "<br>"

                       "<br>"
                       "<img src='https://www.trenitalia.com/content/dam/tcom/immagini/trenitalia-img/offerte-e-servizi/servizi/416x359/416x359-Enjoy-ENI-CarSharing.jpg' width='100' height='100'/>"
        }
    if m.sharing_company == 'Car2go':
        new_marker = {
            'icon': 'https://raw.githubusercontent.com/filippomattio/flaskProject4-gogreen/main/GOGREEN-DEF/sportutilityvehicle.png',
            'lat': m.lat,
            'lng': m.lng,
            'infobox': "<div  ><a class='link_mono' href='https://www.share-now.com/it/it/turin/'>Car2go</a></div>"
                       "<br>"
                       "<form action='/go/Car2go/" + str(m.id) + "'>"
                                                                 "<input type='submit' class='btn btn-primary' value='Reserve now'>"
                                                                 " </form>"
                                                                 "<br>"
                                                                 "<img src='https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Car2go_logo.svg/1200px-Car2go_logo.svg.png' width='100' height='100'/>"
        }
    if m.sharing_company == 'Mobike':
        new_marker = {
            'icon': 'https://raw.githubusercontent.com/filippomattio/flaskProject4-gogreen/main/GOGREEN-DEF/cycling.png',
            'lat': m.lat,
            'lng': m.lng,
            'infobox': "<div  ><a class='link_mono' href='https://it-it.facebook.com/MobikeIT/'>Mobike</a></div>"
                       "<br>"
                       "<form action='/go/Mobike/" + str(m.id) + "'>"
                                                                 "<input type='submit' class='btn btn-primary' value='Reserve now'>"
                                                                 " </form>"
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

        id = int(tt[1])
        sh_co = tt[0]
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
        session['unlock'] = name + "," + str(id)
        st = session['unlock']
        tt = st.split(",")
        id = int(tt[1])
        sh_co = tt[0]
        return redirect(url_for('reservation', name=sh_co, id=id))
    if email and name != 'profile':
        session['unlock'] = name + "," + str(id)
        tr = Transportation(user=email, sharing_company=name, date=datetime.now(), id=id)
        sh = SharingCompany.query.filter_by(name=tr.sharing_company).first()
        session['info'] = tr.user + "," + tr.sharing_company + "," + str(tr.date) + "," + str(tr.id)
        tt=session['unlock']
        reservation_time = sh.reservation_time
        seconds = sh.reservation_time.hour * 3600 + sh.reservation_time.minute * 60 + sh.reservation_time.second
        #db.session.add(tr)
        #db.session.commit()
        flag2.SetFlag(False)
        send_mail(email, "Greengo Reservation", "mailReserve", user=user, transportation=tr,
                  reservation_time=reservation_time)
        return redirect(url_for('setcookie', id=id, name=name, email=email, seconds=seconds))
    """"if 'unlock' in session and flag2.getFlag() == False:

        tr = Transportation.query.filter_by(user=session['email']).order_by(desc(Transportation.date)).first()

        if 'validate' in session:
            session['info'] = tr.user + "," + tr.sharing_company + "," + str(tr.date) + "," + str(tr.id)
        st = session['unlock']
        tt = st.split(",")
        id_reservation = int(tt[1])
        name_reservation = tt[0]

        session['id_first']=tr.id
        session['sc_first'] = tr.sharing_company
        flag2.SetFlag(True)
        db.session.delete(tr)
        db.session.commit()
    elif 'unlock' in session and flag2.getFlag() == True:
        if 'validate' in session:
            session['validate'] = 'True'
        st = session['unlock']
        tt = st.split(",")
        id_reservation = int(tt[1])
        name_reservation = tt[0]

        session['id_first'] = int(tt[1])
        session['sc_first'] = tt[0]
        flag2.SetFlag(True)
   
    else:
        id_reservation = ""
        name_reservation = """""
    if 'unlock' in session:
        st = session['unlock']
        tt = st.split(",")
        id_reservation = int(tt[1])
        name_reservation = tt[0]
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
        if 'delete' not in session:
            id_reservation = ass[0].id
            name_reservation = ass[0].sharing_company

    else:
        ass=[]
    if 'validate' in session:
        st = session['info']
        tt = st.split(",")
        tr = Transportation(user=tt[0], sharing_company= tt[1], date=datetime.strptime(tt[2], '%Y-%m-%d %H:%M:%S.%f'), id=int(tt[3]) )
        db.session.add(tr)
        db.session.commit()
        tr = Transportation.query.filter_by(user=session['email']).order_by(desc(Transportation.date)).first()
        sh_co = SharingCompany.query.filter_by(name=tr.sharing_company).first()
        dict[tr.date] = sh_co
        count = count + 1
        tot = tot + sh_co.price_per_minute
        ass = Transportation.query.filter_by(user=session['email']).order_by(desc(Transportation.date)).all()
        user.points = user.points + sh_co.points
        session.pop('validate', None)
    if 'delete' in session and flag.getFlag() == False:
        session.pop('delete', None)
    if 'delete' in session and flag.getFlag() == True:
        flag.SetFlag(False)

        session.pop('unlock', None)
        session.pop('info', None)

    """if 'delete' in session and flag.getFlag() == False:
        if flag2.getFlag() == False:
            tr = Transportation.query.filter_by(user=session['email']).order_by(desc(Transportation.date)).first()
            flag2.SetFlag(True)
            db.session.delete(tr)
            db.session.commit()
            count = count - 1
            ass = Transportation.query.filter_by(user=session['email']).order_by(desc(Transportation.date)).all()
        session['delete'] = ''
    if 'delete' in session and flag.getFlag() == True:
        if flag2.getFlag() == False:
            tr = Transportation.query.filter_by(user=session['email']).order_by(desc(Transportation.date)).first()
            flag2.SetFlag(True)
            db.session.delete(tr)
            db.session.commit()
            count = count - 1
            ass = Transportation.query.filter_by(user=session['email']).order_by(desc(Transportation.date)).all()
        flag.SetFlag(False)"""
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
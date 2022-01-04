from flask import Flask, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy


from form import LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hard to guess'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///website.db"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)


@app.before_first_request
def create_db():
    db.drop_all()
    db.create_all()




@app.route('/')
def homepage():  # put application's code here
    username = session.get('username')
    return render_template("index.html", username=username)


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    password = None
    username = None
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        session['username'] = username
        return redirect(url_for('homepage'))
    return render_template('login.html', form=form, username=username, password=password)


@app.route('/logout', methods=['POST', 'GET'])
def logout_page():
    session.clear()
    return redirect(url_for('homepage'))


if __name__ == '__main__':
    app.run(debug=True)

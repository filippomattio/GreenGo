from flask import Flask, render_template


from form import LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'hard to guess'

@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")


@app.route('/login',methods=['POST','GET'])
def login_page():
    form = LoginForm()
    password=None
    username=None
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

    return render_template('login.html',form=form, username=username, password=password)

if __name__ == '__main__':
    app.run()

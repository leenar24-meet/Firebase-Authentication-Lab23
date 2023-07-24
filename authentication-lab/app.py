from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
config = {
  "apiKey": "AIzaSyA-_rx6KSqW8BQTikNlmMfqYBVdGgu4BGU",
  "authDomain": "winter-project-31d88.firebaseapp.com",
  "projectId": "winter-project-31d88",
  "storageBucket": "winter-project-31d88.appspot.com",
  "messagingSenderId": "19928945824",
  "appId": "1:19928945824:web:2a205188237a97b2c065c5",
  "measurementId": "G-6FEGKH25VF",
  "databaseURL":"" };


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()



@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method== 'POST':
        email = request.form['email']
        Password = request.form['password']
        try:
            login_session['user'] =auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except: 
            print('the key user isn’t in login_session')
            return redirect(url_for('signin'))
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method== 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
               # return redirect(url_for('home'))
        except: 
            print('the key user isn’t in login_session')
            return redirect(url_for('signin'))


    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)
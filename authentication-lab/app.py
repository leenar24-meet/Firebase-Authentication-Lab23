from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
config = {
  "apiKey": "AIzaSyBCmZHuYpQFMPyopY9ogFkxKAX4quLB978",
  "authDomain": "allawi-11c42.firebaseapp.com",
  "projectId": "allawi-11c42",
  "storageBucket": "allawi-11c42.appspot.com",
  "messagingSenderId": "1070532889920",
  "appId": "1:1070532889920:web:fcd69c7fbc34108c0ffea5",
  "measurementId": "G-L4EZSYCHBB",
  "databaseURL":"https://allawi-11c42-default-rtdb.firebaseio.com/" };


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

# fix the login

@app.route('/', methods=['GET', 'POST'])
def signin():
    try:
        if request.method== 'POST':
            email = request.form['email']
            password = request.form['password']
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
    except: 
        print("the key user isn’t in login_session")
        return redirect(url_for('signin'))
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method== 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user= {"full_name": request.form['full_name'], "username": request.form['username'], "bio": request.form['bio']}
            db.child("Users").child(UID).set(user)
            return redirect(url_for('add_tweet'))
        except Exception as e: 
            print(e)

    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method=="POST":
        try: 
            UID = login_session['user']['localId']
            tweets={"title": request.form['Title'], "text": request.form['Text'], "UID":UID}
            db.child("Tweets").push('tweets')
        except:
            return redirect(url_for('signin'))
    return render_template("add_tweet.html")

@app.route('/all_tweets')
def all_tweets():
    alltweets= db.child("tweets").get().val()
    return render_template("tweets.html")










if __name__ == '__main__':
    app.run(debug=True)
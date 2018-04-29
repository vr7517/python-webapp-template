from flask import Flask, render_template, request
import os, time

app = Flask(__name__)

#############
### LOGIN ###
#############

# # Required for login
from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin
from flask import flash, redirect, url_for, request
from functions.auth_user import auth

# Secret Key to use for login
app.config.update(SECRET_KEY = 'aoun@ibm')

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# user model for login
class User(UserMixin):

    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password
        
    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)

## Login methods ##

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'] 
        success, uid = auth(username, password)    
        if(success):
            login_user(User(uid, username, password))
            flash('Logged in successfully.')
            return redirect(url_for('home'))
        else:
            return abort(401)
    else:
        return render_template("login.html")

#logout API
@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return url_for('login')

# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed, Invalid username or password</p>')

# callback to reload the user object        
@login_manager.user_loader
def load_user(uid):

    return User(1, "aoun", "IBM@123") 

############
### CHAT ###
############

## Chat page ##

@app.route('/chat')
def chat():
    return render_template('chat.html')

## Chat GET Request handler ##

@app.route('/api/message', methods=['GET'])
def message():

    msg = request.args.get('msg')
    print(msg)

    return "Have a reply"

############
### MAIN ###
############

## Main methods ##

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route('/')
def home():
    return render_template('index.html')

## GET Reques handler ## 

@app.route('/api/get-api', methods=['GET'])
def getApi():

    req = request.args.get('request')
    print(req)

    time.sleep(2)

    return "Test Response"


###################################
### POST Request Image Handling ###
###################################
from PIL import Image
import io

@app.route('/api/post-api', methods=['POST'])
def postAPI():

    data = request.files.get('image').read()
    
    image = Image.open(io.BytesIO(data))
    image.save('images/temp.png')
        
    time.sleep(2)
    
    return "Done Saving Image"

## Main ##

if __name__ == '__main__':

    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

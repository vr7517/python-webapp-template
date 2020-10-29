from aadservice import getaccesstoken
from pbiembedservice import getembedparam
from flask import Flask, render_template, request, jsonify,send_from_directory
import json
import os
import requests
import time

# Assistant
from functions.vcap import getService
from watson_developer_cloud import AssistantV1
from functions.auth_user import auth, getUser
from flask import session

# Login
from flask import redirect, url_for, Response, abort, session
from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin

# Image
import io
from PIL import Image


app = Flask(__name__)

#############
### LOGIN ###
#############

# # Required for login

# Secret Key to use for login
app.config.update(SECRET_KEY='aoun@ibm')

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# user model for login


class User(UserMixin):

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return "%d/%s" % (self.id, self.name)

    def get_id(self):
        return self.id

    def is_anonymous(self):
        return False

    def is_active(self):
        return True

## Login methods ##


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        success, uid = auth(username, password)

        if(success):
            login_user(User(uid, username))
            return redirect(url_for('home'))
        else:
            return abort(401)
    else:
        return render_template("login.html")

# logout API


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect('login')

# handle login failed


@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed, Invalid username or password</p>')

# callback to reload the user object


@login_manager.user_loader
def load_user(uid):

    return User(uid, getUser(uid))

############
### CHAT ###
############

# Secret Key to use for session
app.config.update(SECRET_KEY='aoun@ibm')

## Watson Assistant ##
api, url = getService('assistant')

conversation = AssistantV1(
    version='2018-09-20',
    iam_apikey=api,
    url=url
)

## Chat page ##


@app.route('/chat')
def chat():

    session.clear()
    return render_template('chat.html')

## Chat GET Request handler ##


@app.route('/api/message', methods=['POST'])
def message():

    msg = request.form.get('msg')

    if 'context' not in session:
        session['context'] = {}

    if 'input' in msg:
        text = {'text': msg}
    else:
        text = {'text': ''}

    reply = 'Have a reply'

    ## Watson Assistant ##
    try:
        r = conversation.message(
            workspace_id='**************',
            input=text,
            context=session['context']
        ).get_result()

        session['context'] = r['context']
        reply = r['output']['text'][0]

    except Exception as e:
        print(e)
        return repr(e)
    ## Watson Assistant END ##

    return reply

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


# Load configuration
app.config.from_object('config.BaseConfig')

@app.route('/')
def index():
    '''Returns a static HTML page'''

    return render_template('index.html')



@app.route('/getembedinfo', methods=['GET'])
def getembedinfo():
    '''Returns Embed token and Embed URL'''

    configresult = checkconfig()
    if configresult is None:
        try:
            accesstoken = getaccesstoken()
            embedinfo = getembedparam(accesstoken)
        except Exception as ex:
            return json.dumps({'errorMsg': str(ex)}), 500
    else:
        return json.dumps({'errorMsg': configresult}), 500

    return embedinfo

def checkconfig():
    '''Returns a message to user for a missing configuration'''
    if app.config['AUTHENTICATION_MODE'] == '':
        return 'Please specify one the two authentication modes'
    if app.config['AUTHENTICATION_MODE'].lower() == 'serviceprincipal' and app.config['TENANT_ID'] == '':
        return 'Tenant ID is not provided in the config.py file'
    elif app.config['REPORT_ID'] == '':
        return 'Report ID is not provided in config.py file'
    elif app.config['WORKSPACE_ID'] == '':
        return 'Workspace ID is not provided in config.py file'
    elif app.config['CLIENT_ID'] == '':
        return 'Client ID is not provided in config.py file'
    elif app.config['AUTHENTICATION_MODE'].lower() == 'masteruser':
        if app.config['POWER_BI_USER'] == '':
            return 'Master account username is not provided in config.py file'
        elif app.config['POWER_BI_PASS'] == '':
            return 'Master account password is not provided in config.py file'
    elif app.config['AUTHENTICATION_MODE'].lower() == 'serviceprincipal':
        if app.config['CLIENT_SECRET'] == '':
            return 'Client secret is not provided in config.py file'
    elif app.config['SCOPE'] == '':
        return 'Scope is not provided in the config.py file'
    elif app.config['AUTHORITY_URL'] == '':
        return 'Authority URL is not provided in the config.py file'
    
    return None


@app.route('/favicon.ico', methods=['GET'])
def getfavicon():
    '''Returns path of the favicon to be rendered'''

    return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico', mimetype='image/vnd.microsoft.icon')


## GET Request handler ##


@app.route('/api/post', methods=['POST'])
def getApi():

    try:

        print(request.form)
        req = request.form.to_dict()['request']
        print(req)

        time.sleep(2)

        return jsonify({'response': "POST Response"})

    except Exception as e:
        return jsonify({"error": repr(e)})

## GET Request handler ##

@app.route('/api/get', methods=['GET'])
def postApi():

    try:

        req = request.args.get('request')
        print(req)

        time.sleep(2)

        return jsonify({'response': "Get Response"})

    except Exception as e:
        return jsonify({"error": repr(e)})


######################
### Image Handling ###
######################


@app.route('/api/image', methods=['POST'])
def postAPI():

    try:
        data = request.files.get('image').read()

        image = Image.open(io.BytesIO(data))
        image.save('images/temp.png')

        time.sleep(2)

        return jsonify({'response': "Done Saving Image"})

    except Exception as e:
        return jsonify({"error": repr(e)})

## Main ##


if __name__ == '__main__':

    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

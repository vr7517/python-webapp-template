# python-web app-template
A template python web app that includes common web pages. Will be continuously updated.

## Requirements

Written for Python 3 with minimal dependencies (in `requirements.txt`):

* Flask
* (optional - for login) flask-login
* (Optional - for image upload) pillow

## UI

UI content inlcudes:

 * Login
 * Chat
 * Simple Input
 * Image Upload
 
You can remove the UI pages you don't need by removing their relevant files in `templates/`, `static/stylesheets/`, and `static/javascript`. 

![login](images/login.png)
![chat](images/chat.png)
![main](images/main.png)

## Web app

* `app.py` contains the Flask server.
* `functions/` contains utilities and functionalities, this is to be used to avoid cluttering the main app file. 
* The different UI routes (and their relevant methods) are sectioned in `app.py`. You can remove any sections which you don't need.
* APIs: APIs sample is implimented in `/api/...` route, modify te content and/or route name in `app.py ` as per your needs. There is one route to handle a GET request and another route for POST request. The POST request handles image upload through forms.
* Chat: impliment the chat functionality in the `api/message` route in `app.py`.

## Cloud Foundry

The application is CF ready, just type `cf push app-name` after logging in on the cf command line and it should push. 

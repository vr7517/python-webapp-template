# python-web app-template
A template python web app that includes common web pages. Will be continuously updated.

## Requirements

Written for Python 2.7 with minimal dependencies (in `requirements.txt`):

* Flask
* (optional - for login) flask-login

## UI

UI content inlcudes:

 * Login
 * Chat
 * Simple input
 
 You can remove the UI pages you don't need by removing their relevant files in `templates/`, `static/stylesheets/`, and 'static/javascript'. 
 
 ## Web app
 
 * `app.py` contains the Flask server.
 * `functions/` contains utilities and functionalities, this is to be used to avoid cluttering the main app file. 
 * The different UI routes (and their relevant methods) are sectioned in `app.py`. You can remove any sections which you don't need.
 
 ## Cloud Foundry
 
 The application is CF ready, just type `cf push app-name` after logging in on the cf command line and it should push. 

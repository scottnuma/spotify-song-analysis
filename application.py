import os
import spotipy
import spotipy.oauth2 as oauth2
import analysis

from flask import Flask, render_template, redirect, request, send_from_directory

if 'CLIENT_ID' in os.environ:
    CLIENT_ID = os.environ['CLIENT_ID']

if 'CLIENT_SECRET' in os.environ:
    CLIENT_SECRET = os.environ['CLIENT_SECRET']

if 'REDIRECT_URI' in os.environ:
    REDIRECT_URI = os.environ['REDIRECT_URI']

SCOPE = 'user-library-read user-top-read playlist-read-private playlist-read-collaborative'

app = Flask(__name__, static_folder='static')

@app.route('/')
def hello_world():
    return 'hello world!'

@app.route('/analysis')
def analysis():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/static/<path:path>')
def sender(path):
    return send_from_directory(app.static_folder, path)

@app.route('/login/')
def register():
    sp_oauth = oauth2.SpotifyOAuth(
            CLIENT_ID,
            CLIENT_SECRET,
            REDIRECT_URI,
            scope=SCOPE)
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/token')
def receive_token():
    code = request.args.get('code')
    sp_oauth = oauth2.SpotifyOAuth(
            CLIENT_ID,
            CLIENT_SECRET,
            REDIRECT_URI,
            scope=SCOPE)

    token_info = sp_oauth.get_access_token(code)
    user = analysis.User(token_info['access_token'])
    user.record()
    return redirect("http://localhost:8000/static/index.html?username0=%s" % user.username)

if __name__ == "__main__":
    app.run()

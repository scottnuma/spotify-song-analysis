import os
import spotipy
import spotipy.oauth2 as oauth2
import analysis

from flask import Flask, render_template, redirect, request

assert 'CLIENT_ID' in os.environ
CLIENT_ID = os.environ['CLIENT_ID']

assert 'CLIENT_SECRET' in os.environ
CLIENT_SECRET = os.environ['CLIENT_SECRET']

assert 'REDIRECT_URI' in os.environ
REDIRECT_URI = os.environ['REDIRECT_URI']

SCOPE = 'user-library-read user-top-read playlist-read-private playlist-read-collaborative'

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello'

@app.route('/static/<path:path>')
def sender(path):
    return send_from_directory('static', path)

@app.route('/login/')
def register():
    sp_oauth = oauth2.SpotifyOAuth(
            CLIENT_ID,
            CLIENT_SECRET,
            REDIRECT_URI,
            scope=SCOPE)
    auth_url = sp_oauth.get_authorize_url()
    print("Redirecting to %s" % auth_url)
    return redirect(auth_url)

@app.route('/okay')
def okay():
    return "more"

@app.route('/alpha')
def alpha():
    return redirect("http://localhost:8000/static/index.html?username0=%s" % "newmascot")

@app.route('/token')
def receive_token():
    print("Received token")
    code = request.args.get('code')
    sp_oauth = oauth2.SpotifyOAuth(
            CLIENT_ID,
            CLIENT_SECRET,
            REDIRECT_URI,
            scope=SCOPE)

    token_info = sp_oauth.get_access_token(code)
    user = analysis.User(token_info['access_token'])
    user.record()
    print("Recorded - redirecting to viewer")
    return redirect("http://localhost:8000/static/index.html?username0=%s" % user.username)

if __name__ == "__main__":
    app.run(port=8000)

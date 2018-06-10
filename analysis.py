import os
import sys
import spotipy
import spotipy.util as util
import numpy as np
import json

# Retrieve secrets.

assert 'CLIENT_ID' in os.environ
CLIENT_ID = os.environ['CLIENT_ID']

assert 'CLIENT_SECRET' in os.environ
CLIENT_SECRET = os.environ['CLIENT_SECRET']

assert 'REDIRECT_URI' in os.environ
REDIRECT_URI = os.environ['REDIRECT_URI']


# Authenticate with Spotify API

scope = 'user-library-read user-top-read playlist-read-private playlist-read-collaborative'

username = "newmascot"

token = util.prompt_for_user_token(username,
                                   scope,
                                   client_id=CLIENT_ID,
                                   client_secret=CLIENT_SECRET,
                                   redirect_uri=REDIRECT_URI)
if not token:
    print("Unable to get token for", username)
    throw -1

# Initialize the portal into Spotify
sp = spotipy.Spotify(auth=token)

class Song:
    def __init__(this, raw, user_name):
        this.id = raw['id']
        this.name = raw['name']
        this.user_name = user_name

    def __str__(this):
        return this.name

    def __repr__(this):
        return ("Song(%s)" % this.name)

def populate(sp, songs):
    """Batch populate songs with its audio features"""
    org = dict()
    for song in songs:
        org[song.id] = song

    features = sp.audio_features(org.keys())
    for feature_set in features:
        song = org[feature_set['id']]
        song.danceability = feature_set['danceability']
        song.energy = feature_set['energy']
        song.key = feature_set['key']
        song.loudness = feature_set['loudness']
        song.mode = feature_set['mode']
        song.speechiness = feature_set['speechiness']
        song.acousticness = feature_set['acousticness']
        song.instrumentalness = feature_set['instrumentalness']
        song.liveness = feature_set['liveness']
        song.valence = feature_set['valence']
        song.tempo = feature_set['tempo']
        song.duration_ms = feature_set['duration_ms']
        song.time_signature = feature_set['time_signature']


user_name = sp.current_user()['id']
time_frames = ['short_term', 'medium_term', 'long_term']
raw_top_tracks = sp.current_user_top_tracks(limit=50, time_range='long_term')
top_tracks = [Song(track, user_name) for track in raw_top_tracks['items']]
populate(sp, top_tracks)

with open('top_tracks.json', 'w') as fp:
    json.dump([track.__dict__ for track in top_tracks], fp, indent=4)
print("Finished executing")

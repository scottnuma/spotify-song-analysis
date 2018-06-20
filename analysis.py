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

SCOPE = 'user-library-read user-top-read playlist-read-private playlist-read-collaborative'

class User:
    def __init__(this, username):
        this.username = username

        token = util.prompt_for_user_token(this.username,
                                           SCOPE,
                                           client_id=CLIENT_ID,
                                           client_secret=CLIENT_SECRET,
                                           redirect_uri=REDIRECT_URI)
        if not token:
            print("Unable to get token for", username)
            throw -1

        sp = spotipy.Spotify(auth=token)
        time_frames = ['short_term', 'medium_term', 'long_term']
        this.top_tracks = dict()
        for time_frame in time_frames:
            raw_top_tracks = sp.current_user_top_tracks(limit=50, time_range=time_frame)
            this.top_tracks[time_frame] = [Song(track) for track in raw_top_tracks['items']]
            populate(sp, this.top_tracks[time_frame])

    def json(this):
        return json.dumps(this, 
                default=lambda o: o.__dict__, 
                sort_keys=True, 
                indent=4, 
                separators=(',',': '))

    def record(this):
        filename = this.username + ".json"
        with open(filename, 'w') as f:
            f.write(this.json())

class Song:
    def __init__(this, raw):
        this.id = raw['id']
        this.name = raw['name']

    def __str__(this):
        return this.name

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

if __name__ == "__main__":
    user = User("newmascot")
    user.record()

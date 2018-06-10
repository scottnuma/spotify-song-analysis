import os
import sys
import spotipy
import spotipy.util as util
import numpy as np
import matplotlib.pyplot as plt

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

# In[5]:

# Initialize the portal into Spotify
sp = spotipy.Spotify(auth=token)

sp.current_user()
user_name = 'newmascot'

class Song:
    def __init__(this, id, user_name):
        this.id = id
        this.user_name = user_name

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

class SongGroup:
    # Features that are represented by a number
    numerical_features = {
        'acousticness',
        'danceability',
        'duration_ms',
        'energy',
        'instrumentalness',
        'key',
        'liveness',
        'loudness',
        'mode',
        'speechiness',
        'tempo',
        'time_signature',
        'valence'
    }

    # the range of numerical features that are not (0,1)
    feature_range = {
        'key':(0,11),
        'loudness':(-60, 0),
        'tempo':(0,250),
        'time_signature':(0,8),  
        'duration_ms':(0,600000)
    }
    
    def __init__(this, output):
        """ids (list of song ids as strings): songs to be included in the the SongGroup"""
        this.raw = output
        songs = output['items']
        this.song_names = [song['name'] for song in songs]
        this.song_ids = [song['id'] for song in songs]
        feature_aggregate = sp.audio_features(this.song_ids)
        this.feature_names = feature_aggregate[0].keys()
        
        this.feature_dict = dict()
        for feature in this.feature_names:
            this.feature_dict[feature] = np.array([song[feature] for song in feature_aggregate])
            
    def __str__(self):
        return "SongGroup"

time_frames = ['short_term', 'medium_term', 'long_term']
songGroup = SongGroup(sp.current_user_top_tracks(limit=50, time_range='long_term'))

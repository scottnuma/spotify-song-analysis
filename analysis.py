import os
import sys
import spotipy
import spotipy.util as util
import numpy as np
import json

SCOPE = 'user-library-read user-top-read playlist-read-private playlist-read-collaborative'

class User:
    def __init__(this, token):

        sp = spotipy.Spotify(auth=token)
        this.username = sp.current_user()['id']
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
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        subdir = os.path.join("static", "user_tracks")
        filename = this.username + ".json"
        filepath = os.path.join(curr_dir, subdir, filename)
        with open(filepath, 'w') as f:
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
        if feature_set:
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
        else:
            print(feature_set, features, org)

if __name__ == "__main__":
    user = User("newmascot")
    user.record()

from time import time

from database import Database

from match_sample import match_sample
from plot_song import plot_song
from rand_clip import get_digital_recording

import matplotlib.pyplot as plt

import librosa

from const import SAMPLING_RATE

from garbanzo_reader import read_garbanzo

database = Database.get_instance()
database.switch_db("goodone")

# empty database to start with
print(database.list_songs())

# Replace with your own songs

start = time()
dt = time() - start

# database.save()

samps, sr = librosa.load("sturdy-garbanzo/DownbytheRiver.ogg", sr=SAMPLING_RATE, mono=True, duration=30, offset=10)

# samps, sr = get_digital_recording(15)

print("samples", sr)

# plot_song(samps, sampling_rate=sr)
#
match = match_sample(samps, fs=sr)
print(match)

print(database.song_list[match])

plt.show()

from time import time

from database import Database

from match_sample import match_sample

import librosa

from const import SAMPLING_RATE

from garbanzo_reader import read_garbanzo

database = Database.get_instance()

database.switch_db("tutorial1")

# empty database to start with
print(database.list_songs())

# Replace with your own songs





start = time()
#db.add_songs(songs, names, artists)
database.add_songs(songs, names, artists)
dt = time() - start

database.save()

samps, sr = librosa.load("Beatles_TwistAndShout.mp3", sr=44100, mono=True,
                                      offset = 27, duration=10)

match = match_sample(samps, SAMPLING_RATE)
print(match)


# PROVIDED CODE FOR ADDING SONGS TO DATABASE
# songs = [
#     #r"D:\My Music\Pink Floyd Wish You Were Here.mp3",
#     "Beatles_TwistAndShout.mp3"
#     #, r"D:\My Music\JimiHendrix_LittleWing.mp3"
#     ]
#
# names = [
#     #"Wish you were Here",
#     "Twist and Shout"
#     #, "Little Wing"
#     ]
#
# artists = [
#     #"Pink Floyd",
#     "The Beatles"
#     #, "Jimi Hendrix"
#     ]
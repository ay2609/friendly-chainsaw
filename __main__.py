from time import time

from database import Database

database = Database.get_instance()

database.switch_db("tutorial1")

# empty database to start with
print(database.list_songs())

# Replace with your own songs

songs = [r"D:\My Music\Pink Floyd Wish You Were Here.mp3",
         r"D:\My Music\Beatles_TwistAndShout.mp3",
         r"D:\My Music\JimiHendrix_LittleWing.mp3"]

names = ["Wish you were Here", "Twist and Shout", "Little Wing"]

artists = ["Pink Floyd", "The Beatles", "Jimi Hendrix"]

start = time()
#db.add_songs(songs, names, artists)
database.add_songs(songs, names, artists)
dt = time() - start


database.save()
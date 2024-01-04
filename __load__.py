from const import SAMPLING_RATE
from database import Database

from garbanzo_reader import read_garbanzo
from rich.pretty import pprint

database = Database.get_instance()
database.switch_db("goodone")

beans = read_garbanzo()
pprint(beans)

songs = [bean.filename for bean in beans]
titles = [bean.title for bean in beans]
artists = [bean.artist for bean in beans]

input('Press ENTER to continue...')

database.add_songs(songs, titles, artists)

print('Done, saving...')
database.save()

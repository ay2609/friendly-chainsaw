from database import Database
from rich.pretty import pprint

database = Database.get_instance()
database.switch_db("goodone")

songs = database.list_songs()
pprint(songs)

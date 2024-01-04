from const import SAMPLING_RATE

from garbanzo_reader import read_garbanzo
from rich.pretty import pprint

beans = read_garbanzo()
pprint(beans)

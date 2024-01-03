import json
import os
from typing import Iterator
import pathlib

_manifest_path = os.path.join(pathlib.Path(__file__).parent.resolve(), 'sturdy-garbanzo/garbanzo.json')


class Garbanzo:
    def __init__(self, data: dict[str, str]) -> None:
        self.filename = data['file']
        self.title = data.get('title', 'Kyle forgot the title')
        self.artist = data.get('artist', 'Kyle forgot the artist')

    def __repr__(self) -> str:
        return f"<Garbanzo filename={self.filename}, title={self.title} artist={self.artist}>"

    def __str__(self) -> str:
        return repr(self)

    def __iter__(self) -> Iterator[str]:
        yield self.filename
        yield self.title
        yield self.artist


def read_garbanzo() -> list[Garbanzo]:
    with open(_manifest_path, 'r') as f: return [Garbanzo(garbanzo_dict) for garbanzo_dict in json.load(f)]

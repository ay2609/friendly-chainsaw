import pickle
from collections import abc, defaultdict
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Sequence, Tuple, Union

import librosa


PathLike = Union[str, Path]


class Song(NamedTuple):
    song_name: str
    artist: str


class Database:
    """Stores the audio fingerprints associated with songs that have been added to the database"""

    def __init__(self):

        # cwd == current working directory:
        cwd = Path().resolve()
        #self.default_path = Path(__file__).parent / "song_db.pkl"
        self.default_path = cwd / "song_db.pkl"

        self.path: Path = self.default_path
        self.song_list_path = self.path / "_song_list.pkl"

        # See `self.pair_mapping` for details
        self._pair_mapping: Dict[
            Tuple[int, int, int], List[Tuple[int, int]]
        ] = defaultdict(list)

        self._song_list: List[Optional[Tuple[str, Optional[str]]]] = []

        self._loaded = False

    @property
    def song_list(self) -> List[Optional[Tuple[str, Optional[str]]]]:
        """A list of (song-name, artist)

        Items should not be removed from this list! The song-ID in the
        database corresponds to the index of that song's name in this list.
        Instead, a song is removed by replacing its tuple with None"""
        return list(self._song_list)

    @property
    def pair_mapping(self) -> Dict[Tuple[int, int, int], List[Tuple[int, int]]]:
        """Stores the mapping: (f1, f2, dt) -> [(song-ID, t1), ...] where
        (f1, f2, dt) are the frequencies of two peaks and dt is their
        separation in time. [(song-ID, t1), ...] is the list of all song-IDs
        that contain this "fingerprint feature", along with the time at which it
        occurs.

        Note that all frequencies and times are quantized using histogram binning.
        Thus we are able to record an integer - indicating the histogram bin
        location - for each of these values. Multiplying by the bin size will thus
        convert each integer to the corresponding physical quantity"""
        return self._pair_mapping

    def __len__(self) -> int:
        return len(self._song_list)

    def clear(self):
        """Clears the database"""
        self._pair_mapping.clear()
        self._song_list = []
        self._loaded = False

    def switch_db(self, path: Optional[PathLike] = None):
        """Switch the song database being used by specifying its load/save path. Calling this
        function with no argument will revert to the default database.

        Providing a name with no directories will assume database as the directory,
        otherwise the provided path is used. All databases will be saved as .pkl files.

        Parameters
        ----------
        path : PathLike"""

        _backup_db = self._pair_mapping
        _backup_path = self.path
        _loaded = self._loaded

        try:
            if path is not None:
                path = Path(path).resolve()
                parent = (
                    path.parent if str(path.parent) != "." else self.default_path.parent
                )
                self.path = parent / (path.stem + ".pkl")
                assert self.path.parent.exists(), f"{self.path.parent} doesn't exist"
            else:
                self.path = self.default_path
            self._loaded = False
            self._pair_mapping = defaultdict(list)
            self.load()

        except Exception as e:
            print("The following error occurred: {}".format(e))
            print(
                "\nReverting to your prior database state at: {}".format(
                    _backup_path.absolute()
                )
            )
            self._pair_mapping = _backup_db
            self.path = _backup_path
            self._loaded = _loaded
            raise e

    def load(self, force: bool = False):
        """Load the database from database/song_db.pkl if it isn't
        already loaded.

        Call this if you want to load the database up front. Otherwise,
        the other database methods will automatically load it.

        Parameters
        ----------
        force : bool, optional (default=False)
            If `True` the database will be loaded again, even if it
            is already in-memory."""
        if not force and self._loaded:
            return

        if not self.path.is_file():
            print(
                "No song database found. Creating empty database...\n"
                "\tSaving it will save to {}".format(self.path.absolute())
            )
            self._pair_mapping = defaultdict(list)
            self._song_list = []
        else:
            with self.path.open(mode="rb") as f:
                data = pickle.load(f)

            assert isinstance(
                data, defaultdict
            ), f"the loaded database should be a defaultdict, got: {data}"

            self._pair_mapping = data

            with (self.path.parent / (self.path.stem + "_song_list.pkl")).open(
                    mode="rb"
            ) as f:
                song_list = pickle.load(f)

            assert isinstance(
                song_list, list
            ), f"the loaded song_list should be a list, got: {song_list}"

            self._song_list = song_list
            print("song database loaded from: {}".format(self.path.absolute()))
        self._loaded = True

    def remove_song(self, name: str, artist: Optional[str] = None):
        try:
            # do not delete items from song list. song_id in database
            # is determined by song's position in song list. Removing
            # song will create offset in results.
            song_id = self._song_list.index((name, artist))
            self._song_list[song_id] = None

            for key, value in self._pair_mapping.items():
                self._pair_mapping[key] = [x for x in value if x[0] != song_id]

            print("{} removed from database. Be sure to save.".format((name, artist)))
        except ValueError:
            print("{} not in database".format((name, artist)))

    def save(self):
        if self._pair_mapping is None:
            print("No changes to face-database to save")
            return None

        with self.path.open(mode="wb") as f:
            pickle.dump(self._pair_mapping, f)

        with (self.path.parent / (self.path.stem + "_song_list.pkl")).open(
                mode="wb"
        ) as f:
            pickle.dump(self._song_list, f)

        print("Song database saved to: {}".format(self.path.absolute()))

    def add_songs(
            self,
            songs: Union[Path, Sequence[Path]],
            names: Optional[Sequence[str]] = None,
            artists: Optional[Sequence[str]] = None,
            *,
            sampling_rate: int = SAMPLING_RATE,
            min_frac_amp_cutoff: float = MIN_FRAC_AMP_CUTOFF,
            local_peak_nn_radius: int = LOCAL_PEAK_NN_RADIUS,
            fingerprint_fanout: int = FINGERPRINT_FANOUT,
    ):
        """Add songs to the fingerprinting database

        Parameters
        ----------
        songs : Union[Path, Iterable[Path]]
           File path(s) to .mp3, .wav, (and maybe other formats) file(s) to be added.

        names : Optional[Sequence[str | None]]
           Corresponding song names. If `None` is provided, the song name is inferred from
           the filename.

        artists : Optional[Sequence[str | None]]
           Corresponding song artists.

        sampling_rate: int, optional (default=_defaults.SAMPLING_RATE)
            The target sampling rate used to read in an audio file.

        min_frac_amp_cutoff: float, optional (default=_defaults.MIN_FRAC_AMP_CUTOFF)
            The fractional portion of intensities for which the cutoff is selected.
            E.g. frac_cut=0.8 will produce a cutoff intensity such that the bottom 80%
            of intensities are excluded.

        local_peak_nn_radius: int, optional (default=_defaults.LOCAL_PEAK_NN_RADIUS)
            The neighborhood radius used for determining if a spectrogram value
            is a local peak. Specified in spectrogram cells.

        fingerprint_fanout: int, optional (default=_defaults.FINGERPRINT_FANOUT)
            Given a spectrogram peak, indicates the maximum number of subsequent peaks to
            be used to form fingerprint features.

        Notes
        -----
        `add_songs('path/to/song/SongTitle.mp3')` will log this song
        in the database under the title 'SongTitle'."""

        if isinstance(songs, str):
            songs = [songs]

        if names is not None:
            assert isinstance(names, abc.Sequence) and len(names) == len(songs)
        else:
            names = [None] * len(songs)

        if artists is not None:
            assert isinstance(artists, abc.Sequence) and len(artists) == len(songs)
        else:
            artists = [None] * len(songs)

        old_num = len(self._song_list)

        for file_path, name, artist in zip(songs, names, artists):
            song_id = len(self._song_list)
            if name is None:
                name = Path(file_path).name

            if (name, artist) in self._song_list:
                print("{} already in song database. Skipping song.".format(name))
                continue
            print("adding {}..".format(name))

            digital, fs = librosa.load(file_path, sr=sampling_rate, mono=True)
            peaks = local_peaks(
                *digital_to_spec(digital, fs, frac_cut=min_frac_amp_cutoff),
                p_nn=local_peak_nn_radius,
            )

            for f1_f2_dt, t1 in peaks_to_fingerprints(
                    peaks, fan_value=fingerprint_fanout
            ):
                self._pair_mapping[f1_f2_dt].append((song_id, t1))

            self._song_list.append((name, artist))

        if len(self._song_list) - old_num:
            print(
                "{} songs added to the database. "
                "\n\nBe sure to run `database.save()".format(
                    len(self._song_list) - old_num
                )
            )

    def list_songs(self) -> List[Song]:
        sorted_song = sorted(x for x in self._song_list if x is not None)
        return [Song(*x) for x in sorted_song]


database = Database()


def load_song_db(func=None):
    """ This function can be invoked directly to lazy-load the song-recognition database, or it can
    be used as a decorator: the database is lazy-loaded prior to invoking the decorated function.

    See face_rec.face_db._load for more information.

    Parameters
    ----------
    func : Optional[Callable]

    Returns
    -------
    Union[None, Callable]"""
    if func is None:
        database.load()
        return None

    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        database.load()
        return func(*args, **kwargs)
    return wrapper


def switch_db(path=None):
    """ Switch the song database being used by specifying its load/save path. Calling this
    function with no argument will revert to the default database.

    Providing a name with no directories will assume database as the directory,
    otherwise the provided path is used. All databases will be saved as .pkl files.

    Parameters
    ----------
    path : PathLike"""
    database.switch_db(path)


@load_song_db
def clear(x: bool):
    """ Clear the song database.

    You must subsequently run `save_song_database()` to save this change.

    Parameters
    ----------
    x : bool
        Pass True explicitly to confirm that you want to clear the database."""
    assert x is True
    database.clear()


def save():
    """ Save the database."""
    database.save()


@load_song_db
def add_songs(songs, names=None, artists=None):
    """ Add songs to the fingerprinting database

        Parameters
        ----------
        songs : Union[str, Iterable[str]]
           File path(s) to .mp3, .wav, (and maybe other formats) file(s) to be added.

        names : Optional[Sequence[Union[str, None]]]
           Corresponding song names. If `None` is provided, the dong name is inferred from
           the filename.

        artists : Optional[Sequence[Union[str, None]]]
           Corresponding song artists.

        Notes
        -----
        `add_songs_to_database('path/to/song/SongTitle.mp3')` will log this song in the database
        under the title 'SongTitle'. """
    database.add_songs(songs, names=names, artists=artists)


@load_song_db
def list_songs():
    return database.list_songs()


@load_song_db
def remove_song(name, artist=None):
    database.remove_song(name, artist)

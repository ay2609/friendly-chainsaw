from typing import Dict, Iterable, List, Tuple


class FingerprintOffsets:
    def __init__(self, song_id: int, time_offset: float):
        self._song_id = song_id
        self._time_offset = time_offset

    @property
    def song_id(self) -> int:
        return self._song_id

    @property
    def time_offset(self) -> float:
        return self._time_offset

    def __gt__(self, other: 'FingerprintOffsets') -> bool:
        return self.time_offset > other.time_offset

    def __lt__(self, other: 'FingerprintOffsets') -> bool:
        return self.time_offset < other.time_offset


def fingerprints_to_matches(
        sample_fingerprints: Iterable[Tuple[Tuple[int, int, int], int]],
        database: Dict[Tuple[int, int, int], List[Tuple[int, int]]],
) -> Iterable[Tuple[int, float]]:
    """

    kyle

    Generates database matches from all of a sample's fingerprints.

    Parameters
    ----------
    sample_fingerprints : Iterable[Tuple[Tuple[int, int, int], int]]
        ((f_{n}, f_{n+j}, dt), t_{n})
        The frequency value of peak n and peak n+j, along with the time at which peak n occurred.

    database : Dict[Tuple[int, int, int], List[Tuple[Any, int]]
        (freq_{n}, freq_{n+j, dt} -> [(song_ID, t), ... ]
        A dictionary that maps frequency peak-pairs and their offset to a list of all the
        song IDs containing that signature, and the time at which the signature occurred
        in the song.

    Returns
    ------
    Iterable[Tuple[song_ID, dt]]
        An iterable of song IDs that had matching peak-pair signatures, and the time offset between when
        the signature occurred in the song versus the sample."""

    # Student Code:

    matches = []

    for f1_f2_dt, t_sample in sample_fingerprints:
        o = database.get(f1_f2_dt)
        if o is not None:
            for s_id, t_song in o:
                matches.append(s_id, t_song - t_sample)

    return matches




def matches_to_best_match(matches: Iterable[Tuple[int, float]]) -> int:
    """
    Avi & Hunter

    Determines the song-ID that has the most consistent fingerprint-offset

    Parameters
    ----------
    matches : Iterable[Tuple[song_ID, dt]]
        A song-ID that had a match with the sample, and the time-offset between their
        matching signatures.

    Returns
    -------
    SongID
        The song-ID with the most common time-offset with the sample."""

    # Student Code:
    return min([FingerprintOffsets(song_id, offset) for song_id, offset in matches]).song_id

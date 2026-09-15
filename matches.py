from typing import Dict, Iterable, List, Tuple

from database import Database

import numpy as np


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
) -> Iterable[FingerprintOffsets]:
    """
    Generates database matches from all of a sample's fingerprints.

    Parameters
    ----------
    sample_fingerprints : Iterable[Tuple[Tuple[int, int, int], int]]
        ((f_{n}, f_{n+j}, dt), t_{n})
        The frequency value of peak n and peak n+j, along with the time at which peak n occurred.

    Returns
    ------
    Iterable[FingerprintOffsets]
        An iterable of song IDs that had matching peak-pair signatures, and the time offset between when
        the signature occurred in the song versus the sample."""

    counter = np.zeros(len(Database.get_instance().song_list))
    max_fingies = np.zeros_like(counter)

    lol = Database.get_instance().pair_mapping.keys()

    for f1_f2_dt_song in lol:
        for song_id, _ in Database.get_instance()[f1_f2_dt_song]:
            max_fingies[song_id] += 1

    for f1_f2_dt, t_sample in sample_fingerprints:
        for f1_f2_dt_song in lol:
            if abs(f1_f2_dt[0] - f1_f2_dt_song[0]) < 2 and abs(f1_f2_dt[1] - f1_f2_dt_song[1]) < 2 and abs(f1_f2_dt[2] - f1_f2_dt_song[2]) < 2:
            # if f1_f2_dt == f1_f2_dt_song:
                for song_id, _ in Database.get_instance()[f1_f2_dt_song]:
                    counter[song_id] += 1
                # counter[Database.get_instance()[f1_f2_dt_song][0][0]] += 1

    print(max_fingies)
    print(counter)



    return np.array([value/max_fingies[index] for index, value in enumerate(counter)])


def matches_to_best_match(matches: Iterable[FingerprintOffsets]) -> int:
    """
    Avi & Hunter

    Determines the song-ID that has the most consistent fingerprint-offset

    Parameters
    ----------
    matches : Iterable[FingerprintOffsets]
        A song-ID that had a match with the sample, and the time-offset between their
        matching signatures.

    Returns
    -------
    SongID
        The song-ID with the most common time-offset with the sample."""

    # Student Code:

    print(matches)

    return np.argmax(matches)

from typing import Dict, Iterable, List, Tuple, TypeVar

SongID = TypeVar("SongID")


def fingerprints_to_matches(
        sample_fingerprints: Iterable[Tuple[Tuple[int, int, int], int]],
        database: Dict[Tuple[int, int, int], List[Tuple[SongID, int]]],
) -> Iterable[Tuple[SongID, float]]:
    """
    Avi & Hunter

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


def matches_to_best_match(matches: Iterable[Tuple[SongID, float]]) -> SongID:
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


import numpy as np
import random
from collections import Counter
from typing import Dict, Iterable, List, Sequence, Tuple, TypeVar

import matplotlib.mlab as mlab
# from matplotlib.pyplot import Axes, Figure
from numba import njit
from scipy.ndimage.morphology import generate_binary_structure, iterate_structure

SongID = TypeVar("SongID")


def fingerprints_to_matches(
        sample_fingerprints: Iterable[Tuple[Tuple[int, int, int], int]],
        database: Dict[Tuple[int, int, int], List[Tuple[SongID, int]]],
) -> Tuple[SongID, int]:
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

    Yields
    ------
    Tuple[song_ID, dt]
        A song ID that had a matching peak-pair signature, and the time offset between when
        the signature occurred in the song versus the sample."""

    # Student Code:


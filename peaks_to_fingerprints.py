import numpy as np
import random
from collections import Counter
from typing import Dict, Iterable, List, Sequence, Tuple, TypeVar

import matplotlib.mlab as mlab
# from matplotlib.pyplot import Axes, Figure
from numba import njit
from scipy.ndimage.morphology import generate_binary_structure, iterate_structure

SongID = TypeVar("SongID")

def peaks_to_fingerprints(
        peaks: Sequence[Tuple[int, int]], fan_value: int
) -> Iterable[Tuple[Tuple[int, int, int], int]]:
    """
    Avi & Hunter

    Given the time-frequency locations of spectrogram peaks, generates
    'fingerprint' features.

    Parameters
    ----------
    peaks : Sequence[Tuple[int, int]]
        A sequence of time-frequency pairs

    fan_value : int
        Given a peak, `fan_value` indicates the number of subsequent peaks
        to be used to form fingerprint features.

    Yields
    ------
    Tuple[Tuple[int, int, int], int]
        ((f_{n}, f_{n+j}, t_{n+j} - t_{n}), t_{n})
        The frequency value of peak n, peak n+j, their time-offset, along with the
        time at which peak n occurred."""

    # Student Code:

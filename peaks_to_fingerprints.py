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

    Returns
    ------
    Iterable[Tuple[Tuple[int, int, int], int]]
        ((f_{n}, f_{n+j}, t_{n+j} - t_{n}), t_{n})
        The frequency value of peak n, peak n+j, their time-offset, along with the
        time at which peak n occurred.
        """

    fingerprints = []

    for index, (freq, time) in enumerate(peaks):

        if index == len(peaks) - 1:
            pass

        elif fan_value + index > len(peaks) - 1:
            for j in range(len(peaks) - 1 - index):
                fingerprints.append(((freq, peaks[index + j][0], peaks[index + j][1] - time), time))

        else:
            for j in range(fan_value):
                fingerprints.append(((freq, peaks[index + j][0], peaks[index + j][1] - time), time))

    return fingerprints

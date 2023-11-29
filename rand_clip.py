import numpy as np
import random
from collections import Counter
from typing import Dict, Iterable, List, Sequence, Tuple, TypeVar

import matplotlib.mlab as mlab
# from matplotlib.pyplot import Axes, Figure
from numba import njit
from scipy.ndimage.morphology import generate_binary_structure, iterate_structure

SongID = TypeVar("SongID")


def rand_clip(digital: np.ndarray, new: float, fs: int = 44100) -> np.ndarray:
    """
    Nobu

    Produce a random "clip" of a digital signal

    Parameters
    ----------
    digital : numpy.ndarray, shape=(T, )
        digital signal to be clipped

    new : float
        The duration (seconds) of the resulting clip

    fs : int, optional (default=44100)
        The sampling rate of the digital signal

    Returns
    -------
    digital : numpy.ndarray, shape=(T_clipped, )
        Clipped digital signal, sampled from a random starting point"""

    # Student Code:

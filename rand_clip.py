import numpy as np
from pathlib import Path
from typing import Tuple, Union

from matplotlib.pyplot import Axes, Figure

import librosa as _librosa
from microphone import record_audio

def get_digital_recording(time: float) -> Tuple[_np.ndarray, int]:
    """
    Get the digital samples and sampling rate of a microphone's recording.

    Parameters
    ----------
    time : float
        Time, in seconds to record from the mic.

    Returns
    -------
    Tuple[numpy.ndarray, int]
        The digital samples (mono: shape-(N,)) from the recording and
        the sampling rate used.
    """

    # Student Code:

    return digital_data, sample_rate


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

    new_len = int(new * fs)
    start_point = np.random.randint(0, len(digital) - new_len)

    # Extract the clipped signal
    clipped_signal = digital[start_point : start_point + new_len]

    return clipped_signal

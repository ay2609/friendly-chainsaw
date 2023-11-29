from pathlib import Path
from typing import Tuple, Union
from const import *

import numpy as _np
from matplotlib.pyplot import Axes, Figure

import librosa as _librosa
from microphone import record_audio


def get_digital_recording(time: float) -> Tuple[_np.ndarray, int]:
    """
    Nobu

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


@load_song_db
def match_sample(
        sample_digital: _np.ndarray,
        fs: int,
        *,
        min_frac_amp_cutoff: float = MIN_FRAC_AMP_CUTOFF,
        local_peak_nn_radius: int = LOCAL_PEAK_NN_RADIUS,
        fingerprint_fanout: int = FINGERPRINT_FANOUT,
) -> str:
    """
    Kyle

    Given a digital signal, produce the best match from the fingerprint database.

    Parameters
    ----------
    sample_digital : numpy.ndarray, shape=(N,)
        The digital signal

    fs : int
        The sampling rate for the signal

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

    Returns
    -------
    str
        The song-ID for the best match. `None` if no mat"""

    # Student Code:

    return name + ("" if artist is None else " by {}".format(artist))


def match_recording(time: float) -> str:
    """
    Record a song for the specified time, and return the best match from the fingerprint database.

    Parameters
    ----------
    time : float
        The time, in seconds, for which the microphone will record the sample.

    Returns
    -------
    str
        The song-ID for the best match"""
    return match_sample(*get_digital_recording(time))


def plot_song(
        song: Union[str, Path, _np.ndarray],
        with_peaks: bool = True,
        *,
        sampling_rate: int = SAMPLING_RATE,
        min_frac_amp_cutoff: float = MIN_FRAC_AMP_CUTOFF,
        local_peak_nn_radius: int = LOCAL_PEAK_NN_RADIUS,
) -> Tuple[Figure, Axes]:
    """
    Avi

    Plot a spectrogram and fingerprint features for a song.

    Parameters
    ----------
    song : Union[str, pathlib.Path, numpy.ndarray]
        The filepath to a song-file, or the digital signal itself.

    with_peaks : bool
        If True, include peak-value scatter-points

    sampling_rate: int, optional (default=_defaults.SAMPLING_RATE)
        The target sampling rate used to read in an audio file

    min_frac_amp_cutoff: float, optional (default=_defaults.MIN_FRAC_AMP_CUTOFF)
        The fractional portion of intensities for which the cutoff is selected.
        E.g. frac_cut=0.8 will produce a cutoff intensity such that the bottom 80%
        of intensities are excluded.

    local_peak_nn_radius: int, optional (default=_defaults.LOCAL_PEAK_NN_RADIUS)
        The neighborhood radius used for determining if a spectrogram value
        is a local peak. Specified in spectrogram cells.

    Returns
    -------
    Tuple[matplotlib.pyplot.Figure, matplotlib.pyplot.Axes]"""
    from microphone.config import settings
    from pathlib import Path

    # Student Code:

    return fig, ax


def plot_recording(time: float, with_peaks: bool = True) -> Tuple[Figure, Axes]:
    """

    Plot a spectrogram and fingerprint features for a live recording

    Parameters
    ----------
    time : float
        The time, in seconds, for which the microphone will record the sample.

    with_peaks : bool
        If True, include peak-value scatter-points

    Returns
    -------
    Tuple[matplotlib.pyplot.Figure, matplotlib.pyplot.Axes]"""
    digital_data, _ = get_digital_recording(time)
    return plot_song(digital_data, with_peaks=with_peaks)

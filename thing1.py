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


def digital_to_spec(
        digital: np.ndarray, fs: float, frac_cut: float, plot: bool = False
) -> Union[
    Tuple[np.ndarray, float], Tuple[np.ndarray, float, Figure, Axes, float, float]
]:
    """
    Kyl3

    Produces a spectrogram and a cut-off intensity to yield the
    specified fraction of data.

    Parameters
    ----------
    digital : numpy.ndarray, shape=(Ts, )
        The sampled audio-signal.

    fs : float
        The sample-frequency used to create the digital signal.

    frac_cut : float
        The fractional portion of intensities for which the cutoff is selected.
        E.g. frac_cut=0.8 will produce a cutoff intensity such that the bottom 80%
        of intensities are excluded.

    plot : bool
        If True, produce a plot of the spectrogram and return the
        matplotlib fig & ax objects.

    Returns
    -------
    Union[Tuple[numpy.ndarray, float]]
        The spectrogram and the desired cutoff

        If plot=True, then: (spectrogram, cutoff, fig, ax, df, dt)
        is returned. Where (fig, ax) are the plot objects, and df
        and dt are the frequency and time units associated with the
        spectrogram bins.

    Notes
    -----
    One can identify a sensible threshold percentile by consulting the CDF
    of an ensemble of song spectrograms.
    """
    # Student Code:

    # Hint: log-scaled Fourier amplitudes have a much more gradual distribution
    # for audio data.
    # Student Code:

    # Compute percentile-based threshold amplitude; this is greatly optimized by
    # leveraging the apt numpy.partition function.
    # Student Code:

    if not plot:
        return S, cutoff
    else:
        df = freqs[1] - freqs[0]
        dt = times[1] - times[0]
        return S, cutoff, fig, ax, df, dt


@njit()
def _peaks(spec, rows, cols, amp_min):
    """
    Kyle & Nobu

    :param spec:
    :param rows:
    :param cols:
    :param amp_min:
    :return:
    """
    peaks = []
    # We want to iterate over the array in column-major
    # order so that we order the peaks by time. That is,
    # we look for nearest neighbors of increasing frequencies
    # at the same times, and then move to the next time bin.
    # This is why we use the reversed-shape

    # Student Code:

    return peaks


def local_peaks(
        log_spectrogram: np.ndarray, amp_min: float, p_nn: int
) -> List[Tuple[int, int]]:
    """
    Kyle & Nobu

    Defines a local neighborhood and finds the local peaks
    in the spectrogram, which must be larger than the
    specified `amp_min`.

    Parameters
    ----------
    log_spectrogram : numpy.ndarray, shape=(n_freq, n_time)
        Log-scaled spectrogram. Columns are the periodograms of
        successive segments of a frequency-time spectrum.

    amp_min : float
        Amplitude threshold applied to local maxima

    p_nn : int
        The neighborhood radius used for determining if a spectrogram value
        is a local peak. Specified in spectrogram cells.

    Returns
    -------
    List[Tuple[int, int]]
        Time and frequency index-values of the local peaks in spectrogram.
        Sorted by ascending frequency and then time.

    Notes
    -----
    The local peaks are returned in column-major order for the spectrogram.
    That is, the peaks are ordered by time. That is, we look for nearest
    neighbors of increasing frequencies at the same times, and then move to
    the next time bin.
    """
    # Student Code:

    # center neighborhood indices around center of neighborhood

    # Extract peaks; encoded in terms of time and freq bin indices.
    # dt and df are always the same size for the spectrogram that is produced,
    # so the bin indices consistently map to the same physical units:
    # t_n = n*dt, f_m = m*df (m and n are integer indices)
    # Thus we can codify our peaks with integer bin indices instead of their
    # physical (t, f) coordinates. This makes storage and compression of peak
    # locations much simpler.

    return detected_peaks


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

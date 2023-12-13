import numpy as np
import random
from collections import Counter
from typing import Dict, Iterable, List, Sequence, Tuple, TypeVar

import matplotlib.mlab as mlab
# from matplotlib.pyplot import Axes, Figure
from numba import njit
from scipy.ndimage.morphology import generate_binary_structure, iterate_structure

SongID = TypeVar("SongID")

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

    # Iterate over the 2-D data in col-major order
    # we want to see if there is a local peak located at
    # row=r, col=c
    for c, r in np.ndindex(*spec.shape[::-1]):
        if spec[r, c] <= amp_min:
            # The amplitude falls beneath the minimum threshold
            # thus this can't be a peak.
            continue

        # Iterating over the neighborhood centered on (r, c)
        # dr: displacement from r
        # dc: discplacement from c
        for dr, dc in zip(rows, cols):
            if dr == 0 and dc == 0:
                # This would compare (r, c) with itself.. skip!
                continue

            if not (0 <= r + dr < spec.shape[0]):
                # neighbor falls outside of boundary
                continue

            # mirror over array boundary
            if not (0 <= c + dc < spec.shape[1]):
                # neighbor falls outside of boundary
                continue

            if spec[r, c] < spec[r + dr, c + dc]:
                # One of the amplitudes within the neighborhood
                # is larger, thus data_2d[r, c] cannot be a peak
                break
        else:
            # if we did not break from the for-loop then (r, c) is a peak
            peaks.append((r, c))

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

    rows, cols = np.where(amp_min)
    assert amp_min.shape[0] % 2 == 1
    assert amp_min.shape[1] % 2 == 1

    # center neighborhood indices around center of neighborhood
    rows -= amp_min.shape[0] // 2
    cols -= amp_min.shape[1] // 2

    return _peaks(log_spectrogram, rows, cols, amp_min=amp_min)

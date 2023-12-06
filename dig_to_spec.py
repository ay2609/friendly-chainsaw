import numpy as np
import random
from collections import Counter
from typing import Dict, Iterable, List, Sequence, Tuple, TypeVar

import matplotlib.mlab as mlab
# from matplotlib.pyplot import Axes, Figure
from numba import njit
from scipy.ndimage.morphology import generate_binary_structure, iterate_structure

SongID = TypeVar("SongID")

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


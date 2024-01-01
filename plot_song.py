import matplotlib.pyplot as plt
import matplotlib
import numpy as np

from const import MIN_FRAC_AMP_CUTOFF, LOCAL_PEAK_NN_RADIUS, SAMPLING_RATE

from typing import Union, Tuple
from pathlib import Path


def plot_song(
        song: Union[str, Path, np.ndarray],
        with_peaks: bool = True,
        *,
        sampling_rate: int = SAMPLING_RATE,
        min_frac_amp_cutoff: float = MIN_FRAC_AMP_CUTOFF,
        local_peak_nn_radius: int = LOCAL_PEAK_NN_RADIUS,
) -> Tuple[matplotlib.figure, matplotlib.axes]:
    """

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
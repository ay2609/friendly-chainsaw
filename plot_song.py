import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib
import numpy as np
import librosa
from mygrad import sliding_window_view

from const import MIN_FRAC_AMP_CUTOFF, LOCAL_PEAK_NN_RADIUS, SAMPLING_RATE, FINGERPRINT_FANOUT
from microphone.config import settings

from typing import Union, Tuple
from pathlib import Path

from dig_to_spec import digital_to_spec
from rand_clip import get_digital_recording
from peaks import local_peaks
from peaks_to_fingerprints import peaks_to_fingerprints


def plot_song(
        song: Union[str, Path, np.ndarray],
        with_peaks: bool = True,
        *,
        sampling_rate: int = SAMPLING_RATE,
        min_frac_amp_cutoff: float = MIN_FRAC_AMP_CUTOFF,
        local_peak_nn_radius: int = LOCAL_PEAK_NN_RADIUS,
): # -> matplotlib.figure, matplotlib.axes:
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

    spectrogram, cutoff, fig, ax, window_df, window_dt = digital_to_spec(song, fs=sampling_rate, frac_cut=min_frac_amp_cutoff, plot=True)

    cutting = int(np.max(np.log(spectrogram) - np.median(np.log(spectrogram))) * min_frac_amp_cutoff)

    # print("max", np.max(np.log(spectrogram) - np.median(np.log(spectrogram))))

    peaks = local_peaks(np.log(spectrogram) - np.median(np.log(spectrogram)), cutting, local_peak_nn_radius)

    plotted_peaks = np.array([(window_dt * time, window_df * freq) for freq, time in peaks])

    if plotted_peaks != []:
        plt.gca().scatter(plotted_peaks[:, 0], plotted_peaks[:, 1], c='r')

    fingerprints = peaks_to_fingerprints(peaks, fan_value=FINGERPRINT_FANOUT)

    print("peek", peaks)

    return fig, ax


song, s_rate = get_digital_recording(1) # librosa not working, recordings not working
song, s_rate = librosa.load("trumpet.wav", sr=44100, mono=True)

fig, ax = plot_song(song)

plt.show()


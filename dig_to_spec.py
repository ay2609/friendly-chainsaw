import numpy as np

import matplotlib.pyplot as plt

from matplotlib.pyplot import Axes, Figure
from scipy.signal import spectrogram
from mygrad import sliding_window_view


def digital_to_spec(
    digital: np.ndarray, fs: float, frac_cut: float, plot: bool = False
) -> tuple[np.ndarray, float] | tuple[np.ndarray, float, Figure, Axes, float, float]:
    """
    Nobu

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

    window_dt = (1000 / fs)  # dt is constant

    window_size = int(window_dt * fs)

    windowed_audio = sliding_window_view(
        digital, window_shape=(window_size,), step=window_size
    )

    M, N = windowed_audio.shape

    ck_for_each_window = np.fft.rfft(windowed_audio, axis=-1)
    ak_for_each_window = np.absolute(ck_for_each_window) / N
    ak_for_each_window[:, 1: (-1 if N % 2 == 0 else None)] *= 2
    spectrogram = ak_for_each_window.T

    T = len(digital) / fs

    F = (window_size // 2 + 1) / window_dt

    max_freq = 4000

    window_df = (len(digital) / fs) / (fs // 2)

    extent = (0, T, 0, F)
    aspect_ratio = T / max_freq

    fig, ax = plt.subplots()

    ax.imshow(
        np.log(spectrogram),
        origin="lower",
        aspect=aspect_ratio,
        extent=extent,
        interpolation="bilinear",
    )

    ax.set_ylim(0, max_freq)

    ax.set_xlabel("Time (sec)")
    ax.set_ylabel("Frequency (Hz)")
    ax.set_title("Spectrogram of Recording")

    flatten = spectrogram.flatten()
    sortedd = np.sort(flatten)[::-1]

    index = int(len(sortedd) * frac_cut)
    cutoff = sortedd[index]


    if not plot:
        return spectrogram, cutoff
    else:
        return spectrogram, cutoff, fig, ax, window_df, window_dt

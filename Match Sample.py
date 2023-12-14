from pathlib import Path
from typing import Tuple, Union

import numpy as _np
from matplotlib.pyplot import Axes, Figure

import librosa as _librosa
from microphone import record_audio


def match_sample(
    sample_digital: _np.ndarray,
    fs: int,
    *,
    min_frac_amp_cutoff: float = MIN_FRAC_AMP_CUTOFF,
    local_peak_nn_radius: int = LOCAL_PEAK_NN_RADIUS,
    fingerprint_fanout: int = FINGERPRINT_FANOUT,
) -> str:

    """
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

    # take random sample of the full original sample
    rc = rand_clip(sample_digital, 5)

    # create a spectrogram from the random sample
    spec = dig_to_spec(rc)

    # take the peaks of the spectrogram
    ps = local_peaks(spec)

    # form fingerprints based on the peaks
    fins = peaks_to_fingerprints(ps)

    # match the fingerprints from the sample to fingerprints from the database






    return name + ("" if artist is None else " by {}".format(artist))
import numpy as _np

from const import MIN_FRAC_AMP_CUTOFF, LOCAL_PEAK_NN_RADIUS, FINGERPRINT_FANOUT, SAMPLING_RATE
from dig_to_spec import digital_to_spec
from peaks import local_peaks
from peaks_to_fingerprints import peaks_to_fingerprints
from rand_clip import rand_clip
from matches import fingerprints_to_matches
from matches import matches_to_best_match

def match_sample(
        sample_digital: _np.ndarray,
        fs: int = SAMPLING_RATE,
        *,
        min_frac_amp_cutoff: float = MIN_FRAC_AMP_CUTOFF,
        local_peak_nn_radius: int = LOCAL_PEAK_NN_RADIUS,
        fingerprint_fanout: int = FINGERPRINT_FANOUT,
) -> str:
    """
    Given a digital signal, produce the best match from the fingerprint database.

    Parameters
    ----------
    sample_digital : numpy.ndarray, shape=(N, )
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
        The song-ID for the best match. `None` if no match"""

    # Student Code:

    # take random sample of the full original sample
    rc = rand_clip(sample_digital, 5, fs)

    # create a spectrogram from the random sample
    spec, cutoff = digital_to_spec(rc, fs, frac_cut=min_frac_amp_cutoff, plot=False)

    # take the peaks of the spectrogram
    ps = local_peaks(spec, 0, local_peak_nn_radius)

    # form fingerprints based on the peaks
    fins = peaks_to_fingerprints(ps, fingerprint_fanout)

    # match the fingerprints from the sample to fingerprints from the database
    name = matches_to_best_match(fingerprints_to_matches(fins))

    return (name)

    #code to also return artist:
     # + ("" if artist is None else " by {}".format(artist)))

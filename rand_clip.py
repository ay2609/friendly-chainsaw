import numpy as np


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

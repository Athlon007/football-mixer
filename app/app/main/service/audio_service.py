import librosa
import librosa.display
import librosa.feature
import matplotlib.pyplot as plt
import numpy as np
from flask_restx import Namespace


def transform_audio_to_spectrogram(y, sr):
    # Generate the Mel spectrogram
    S = librosa.feature.melspectrogram(y, sr=sr, n_mels=128)

    # Convert to log scale (dB). We'll use the peak power (max) as reference.
    log_S = librosa.power_to_db(S, ref=np.max)

    # Return the spectrogram
    return log_S

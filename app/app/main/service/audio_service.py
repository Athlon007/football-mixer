import librosa.display
import librosa.feature
import cv2
import librosa
import numpy as np
from scipy.signal import spectrogram


def transform_audio_to_spectrogram(y, sr):
    # Generate the Mel spectrogram
    # S = librosa.feature.melspectrogram(y, sr=sr, n_mels=128)
    __S = spectrogram(y)[2]

    # Convert to log scale (dB). We'll use the peak power (max) as reference.
    log_S = librosa.power_to_db(__S, ref=np.max)

    # Rescale to 0-255 range
    scaled_spectrogram = cv2.normalize(log_S, None, 0, 255, cv2.NORM_MINMAX)

    # Convert to uint8
    uint8_spectrogram = scaled_spectrogram.astype(np.uint8)

    # Resize the image to match the output size of 100x100
    resized_spectrogram = cv2.resize(uint8_spectrogram, (100, 100))

    return resized_spectrogram
import librosa.display
import librosa.feature
import cv2
import librosa
import numpy as np
from scipy.signal import spectrogram
import soundfile as sf
from PIL import Image
from .. import ml_model

def resize_spectrogram_image(image, target_size=(100, 100)):
    # Convert to PIL Image
    image_pil = Image.fromarray(image.astype('uint8'))

    # Resize the image
    image_resized = image_pil.resize(target_size)

    # Convert to RGB mode
    image_resized = image_resized.convert('RGB')

    # Convert back to numpy array
    image_resized_np = np.array(image_resized)

    return image_resized_np


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


def process_audio_stream(audio_file, callback):
    y, sr = sf.read(audio_file)
    CHUNK_SIZE = sr 

    for start in range(0, len(y), CHUNK_SIZE):
        end = start + CHUNK_SIZE
        audio_data = y[start:end]
        if len(audio_data) < CHUNK_SIZE:
            audio_data = np.pad(audio_data, (0, CHUNK_SIZE - len(audio_data)), mode='constant')
        
        spectrogram = transform_audio_to_spectrogram(audio_data, sr)

        prediction = callback(spectrogram)

        print(prediction) 
        
    print("Processing complete.")
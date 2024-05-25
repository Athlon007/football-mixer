import librosa.display
import librosa.feature
import cv2
import librosa
import numpy as np
from scipy.signal import spectrogram


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
    y, sr = librosa.load(audio_file, sr=None)  # Load audio with original sampling rate
    CHUNK_SIZE = int(0.08 * sr)  # Define chunk size of 3 seconds

    for start in range(0, len(y), CHUNK_SIZE):
        end = start + CHUNK_SIZE
        audio_data = y[start:end]
        if len(audio_data) < CHUNK_SIZE:
            audio_data = np.pad(audio_data, (0, CHUNK_SIZE - len(audio_data)), mode='constant')

        spectrogram = transform_audio_to_spectrogram(audio_data, sr)

        prediction = callback(spectrogram)

        if prediction.argmax() == 0:
            result = "Ball detected...Volume UP"
        elif prediction.argmax() == 1:
            result = "Whistle detected...Volume UP"
        else:
            result = "Unknown sound detected...Volume DOWN"

        output = {'result': result, 'prediction': prediction.tolist()}
        print(output)
        # return output

    print("Processing complete.")
    return {'message': 'Processing complete'}

BUFFER_SIZE = 3  # Buffer size in seconds
SAMPLE_RATE = 22050  # Example sample rate, should match your audio input

# Buffer to hold incoming audio data
audio_buffer = np.array([])

def process_audio_stream_new(audio_data, callback):
    global audio_buffer
    audio_buffer = np.concatenate((audio_buffer, audio_data))

    result = "No prediction"
    prediction_list = []

    CHUNK_SIZE = BUFFER_SIZE * SAMPLE_RATE
    while len(audio_buffer) >= CHUNK_SIZE:
        chunk = audio_buffer[:CHUNK_SIZE]
        audio_buffer = audio_buffer[CHUNK_SIZE:]

        spectrogram = transform_audio_to_spectrogram(chunk, SAMPLE_RATE)

        # save spectogram into /temp
        unix_timestamp = int(time.time())
        #Image.fromarray(spectrogram.astype('uint8')).convert('RGB').save('temp/spectrogram' + str(unix_timestamp) + '.png')

        prediction = callback(spectrogram)

        if prediction.argmax() == 0:
            result = "Ball detected...Volume UP"
        elif prediction.argmax() == 1:
            result = "Whistle detected...Volume UP"
        else:
            result = "Unknown sound detected...Volume DOWN"

        prediction_list = prediction.tolist()

        print(result)
        print(prediction)

    return {'result': result, 'prediction': prediction_list}

# def transform_audio_to_spectrogram(y, sr):
#     # Generate the Mel spectrogram
#     # S = librosa.feature.melspectrogram(y, sr=sr, n_mels=128)
#     S = spectrogram(y)[2]

#     # Convert to log scale (dB). We'll use the peak power (max) as reference.
#     log_S = librosa.power_to_db(S, ref=np.max)
#     return resized_spectrogram

def process_audio_stream_newest(audio_data, callback, sample_rate):
    global audio_buffer
    audio_buffer = np.concatenate((audio_buffer, audio_data))
    

    result = "No prediction"
    prediction_list = []

    CHUNK_SIZE = BUFFER_SIZE * sample_rate
    while len(audio_buffer) >= CHUNK_SIZE:
        chunk = audio_buffer[:CHUNK_SIZE]
        audio_buffer = audio_buffer[CHUNK_SIZE:]

        spectrogram = transform_audio_to_spectrogram(chunk, sample_rate)

        # Convert spectrogram to uint8 image for saving
        spectrogram_img = (spectrogram / spectrogram.max() * 255).astype('uint8')
        unix_timestamp = int(time.time())
        Image.fromarray(spectrogram_img).convert('RGB').save('temp/spectrogram' + str(unix_timestamp) + '.png')

        prediction = callback(spectrogram)

        if prediction.argmax() == 0:
            result = "Ball detected...Volume UP"
        elif prediction.argmax() == 1:
            result = "Whistle detected...Volume UP"
        else:
            result = "Unknown sound detected...Volume DOWN"

        prediction_list = prediction.tolist()

        print(result)
        print(prediction)

    return {'result': result, 'prediction': prediction_list}

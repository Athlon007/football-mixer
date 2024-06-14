import librosa.display
import librosa.feature
import cv2
import librosa
import numpy as np
from scipy.signal import spectrogram


def resize_spectrogram_image(image, target_size=(100, 100)):
## Here a function that resizes the image to the target size of 100x100 pixels is defined.    

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
    ## Here a function that transforms the audio data into a spectrogram image is defined.
    
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

def filter_audio_data(audio_files, callback):
    ## Here a function that filters the audio data is defined.
    #future_to_index = {executor.submit(process_audio_stream, audio_file, callback, index): index for index, audio_file in enumerate(audio_files)}
    
    #return None
    
    #iterate through audio files using their index , and compare the results of the process_audio_stream function
    results = []
    for index, audio_file in enumerate(audio_files):
        result = process_audio_stream(audio_file, callback, index)
        results.append(result) 
    

def process_audio_stream(audio_file, callback, file_index):
    ## this function processes the audio stream and returns the results with the file index.
    y, sr = librosa.load(audio_file, sr=None)  # Load audio with original sampling rate
    CHUNK_SIZE = int(0.08 * sr)  # Define chunk size of 80 milliseconds

    results = []
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
        results.append(output)
        
        chunk_size = start // CHUNK_SIZE
        print(f"File {file_index} Chunk {chunk_size}: {output}")

    print(f"Processing complete for file {file_index}.")
    return file_index, results

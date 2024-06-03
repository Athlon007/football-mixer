from flask_restx import Resource, Namespace, reqparse
import librosa
import numpy as np
from PIL import Image
import werkzeug.datastructures
from app.main.service.model_service import ml_model
from ..service.audio_service import transform_audio_to_spectrogram, process_audio_stream, filter_audio_data
import concurrent.futures

api = Namespace('predict', description='Prediction related operations')

# Define the file upload parser
file_upload_parser = reqparse.RequestParser()
file_upload_parser.add_argument('file',
                                type=werkzeug.datastructures.FileStorage,
                                location='files',
                                required=True,
                                help='WAV audio file',
                                action='append')
# add batch_id to the parser
file_upload_parser.add_argument('batch_id',
                                type=str,
                                location='form',
                                required=True,
                                help='Batch ID for the audio files')



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

@api.route('/start')
class StartMix(Resource):
    @api.expect(file_upload_parser)
    def post(self):
        args = file_upload_parser.parse_args()
        audio_files = args['file']

        # print count of audio files
        print(f"Number of audio files: {len(audio_files)}")

        batch_id = args['batch_id']
        results = {}

        def callback(spectrogram):
            resized_spectrogram = resize_spectrogram_image(spectrogram)
            resized_spectrogram = resized_spectrogram.astype(np.float32) / 255.0
            prediction = ml_model.predict(np.expand_dims(resized_spectrogram, axis=0))
            return prediction

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_index = {executor.submit(process_audio_stream, audio_file, callback, index): index for index, audio_file in enumerate(audio_files)}
            #future_to_index = {executor.submit(filter_audio_data, audio_files, callback)}

            for future in concurrent.futures.as_completed(future_to_index):
                file_index = future_to_index[future]
                try:
                    index, file_results = future.result()
                    results[index] = file_results
                except Exception as exc:
                    print(f"File {file_index} generated an exception: {exc}")

        # Analyze results to determine the best source to listen to
        # Dummy logic for determining the best audio source
        print('=== Results ===')
        print(results)
        best_source = max(results, key=lambda k: results[k][0]['prediction'][0])
        best_output = results[best_source]

        return { "batch_id": batch_id, "message": "Audio processing completed", "best_source": best_source, "best_output": best_output }, 200


@api.route('/predict')
class Predict(Resource):
    """
        Predict Resource
    """

    @api.expect(file_upload_parser)
    def post(self):
        args = file_upload_parser.parse_args()
        audio_file = args['file']

        # Read the audio data from the FileStorage object and get
        # the sample rate
        y, sr = librosa.load(audio_file)

        # Now you can use the audio data and sample rate in your method
        spectrogram_image = transform_audio_to_spectrogram(y, sr)

        # Resize the spectrogram image to match the model's input shape
        resized_spectrogram = resize_spectrogram_image(spectrogram_image)

        # Convert to float32 and normalize if required
        # Normalizing to [0, 1]
        resized_spectrogram = resized_spectrogram.astype(np.float32) / 255.0

        prediction = ml_model.predict(
            np.expand_dims(resized_spectrogram, axis=0)
            ).tolist()

        print("Prediction done")
        # Save the spectrogram image
        Image.fromarray(spectrogram_image.astype('uint8')) \
            .convert('RGB') \
            .save('spectrogram.png')

        return {'prediction': prediction}, 200
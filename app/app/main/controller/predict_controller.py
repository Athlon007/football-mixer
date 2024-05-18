from flask_restx import Resource, Namespace, reqparse
import librosa
import numpy as np
from PIL import Image
import werkzeug.datastructures
from .. import ml_model
from ..service.audio_service import transform_audio_to_spectrogram, process_audio_stream,resize_spectrogram_image

api = Namespace('predict', description='Prediction related operations')

# Define the file upload parser
file_upload_parser = reqparse.RequestParser()
file_upload_parser.add_argument('file',
                                type=werkzeug.datastructures.FileStorage,
                                location='files',
                                required=True,
                                help='WAV audio file')



@api.route('/')
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
    

@api.route('/start')
class StartMix(Resource):
    """
        Start mixing audio
    """
    @api.expect(file_upload_parser)
    def post(self):
        args = file_upload_parser.parse_args()
        audio_file = args['file']

        def callback(spectrogram):
            # Example callback function using the ML model
            resized_spectrogram = resize_spectrogram_image(spectrogram)
            resized_spectrogram = resized_spectrogram.astype(np.float32) / 255.0
            prediction = ml_model.predict(np.expand_dims(resized_spectrogram, axis=0))
            return prediction

        process_audio_stream(audio_file, callback)
        return {"message": "Audio processing started"}, 200

        
from flask import request
from flask_restx import Resource, Namespace
import librosa

from .. import socketio
from ..service.audio_service import transform_audio_to_spectrogram
from .. import ml_model

api = Namespace('predict', description='prediction related operations')

from werkzeug.datastructures import FileStorage
from flask_restx import reqparse

file_upload_parser = reqparse.RequestParser()
file_upload_parser.add_argument('file',
                                type=FileStorage,
                                location='files',
                                required=True,
                                help='Audio file')


@api.route('/predict')
class Predict(Resource):
    """
        Predict Resource
    """

    @api.expect(file_upload_parser)
    def post(self):
        args = file_upload_parser.parse_args()
        audio_file = args['file']

        # Read the audio data from the FileStorage object and get the sample rate
        y, sr = librosa.load(audio_file)

        # Now you can use the audio data and sample rate in your method
        spectrogram_image = transform_audio_to_spectrogram(y, sr)
        prediction = ml_model.predict(spectrogram_image)

        # download image
        spectrogram_image.save('spectrogram.png')
        return {'prediction': prediction}, 200

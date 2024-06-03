"""
Models Controller
"""
from flask import request
from flask_restx import Resource
from app.main.service.model_service import list_models, load_ml_model
from app.main.dto.model_dto import ModelDTO

api = ModelDTO.api
model_name_schema = ModelDTO.model_name_schema

@api.route('/')
class ModelsList(Resource):
    """
        Returns a list of models available in the system
    """
    @api.doc('Get available models and currently used model')
    def get(self) -> Resource:
        response = list_models()
        return response

@api.route('/set', methods=['POST'])
class ModelsSet(Resource):
    @api.doc('Set the currently used model')
    @api.expect(model_name_schema)
    def post(self) -> Resource:
        model_name = request.json['model_name']
        response = load_ml_model(model_name)
        return response
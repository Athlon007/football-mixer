"""
Model Data Transfer Object
"""

from flask import request
from flask_restx import Namespace, fields

class ModelDTO:
    """
    Model Data Transfer Object
    """
    api = Namespace("model", description="Model related operations")

    model_name_schema = api.model(
        "Set Model Name Schema",
        {
            "model_name": fields.String(required=True, description="""
                                        Name of the model to set. Must be one of the available models.
                                        See GET /models endpoint for a list of available models.
                                        """)
        }
    )

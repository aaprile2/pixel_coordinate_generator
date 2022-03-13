''' DEFINE APP '''

from flask import Flask
from flask_restful import Api
from api.resources.coordinates import Coordinates
from api.resources.plot import Plot


# Application factory
def create_app():
# Instantiate Flask
    app = Flask(__name__)
    api = Api(app)

    # Attach Resource classes to endpoints
    api.add_resource(Coordinates, '/compute_coordinates')
    api.add_resource(Plot, '/plot_solution')

    return app



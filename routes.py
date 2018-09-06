from flask import Blueprint
from flask_restplus import Api, Resource
from app_api.controller.population_controller import PopulationController
from app_api.helpers.my_json_encoder import MyJsonEncoder
import json

routes = Blueprint('routes', __name__)
api = Api(routes)
my_json_encoder = MyJsonEncoder()


@api.route('/get-population')
class GetPopulation(Resource):
    def get(self):
        population_controller = PopulationController()
        population = population_controller.build_population()
        result = my_json_encoder.encode(population).replace("\'", '"')

        return json.loads(result)

# @api.route('/groups')
# class Groups:
#     def get(self):
#         pass
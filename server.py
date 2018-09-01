from flask import Flask
from flask_restplus import Api, Resource

from controller.population_controller import PopulationController
from helpers.my_json_encoder import MyJsonEncoder
import json

app = Flask(__name__)
api = Api(app)


@api.route('/get-population')
class GetPopulation(Resource):
    def get(self):
        my_encoder = MyJsonEncoder()
        population_controller = PopulationController()
        population = population_controller.build_population()
        result = my_encoder.encode(population).replace("\'", '"')

        return json.loads(result)


if __name__ == '__main__':
    app.run(debug=True)

import json
import os


def load_data():
    json_path = '/home/mallmann/TG/FlaskApp/app_api/helpers/names.json'
    # path = os.path.dirname(__name__)
    # path = os.path.join(path, 'names.json')
    with open(json_path, 'r') as f:
        return json.load(f)


class PersonNames(object):
    def __init__(self):
        self.data_from_json = load_data()

    def search_name_by_id(self, person_id):
        for person_name_json in self.data_from_json:
            if person_name_json['person_id'] == person_id:
                return person_name_json['name']

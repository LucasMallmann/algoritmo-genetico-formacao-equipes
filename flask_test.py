from flask import Flask
from flask_restplus import Api, Resource, fields

app = Flask(__name__)
api = Api(app)

a_language = api.model('Language', {
    'language': fields.String('The language')
})

languages = []
python = {'language': 'Python'}
languages.append(python)


@api.route('/language')
class Language(Resource):

    def get(self) -> list:
        return languages

    @api.expect(a_language)
    def post(self) -> object:
        languages.append(api.payload)
        return {'result': 'language added'}, 201


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class Healthcheck(Resource):
    def get(self):
        return {'status': 'ok'}

class Authenticate(Resource):
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        # Authenticate the user and return an access token
        #...
        return {'access_token': 'ome_token'}

api.add_resource(Healthcheck, '/api/healthcheck')
api.add_resource(Authenticate, '/api/authenticate')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
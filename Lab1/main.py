from flask import Flask, jsonify, request
from werkzeug.routing import BaseConverter, ValidationError


_USERS = {'1': 'Francesco' , '2': 'Daniele' , '3': 'Prati'}
_IDS = {val : id for id,val in _USERS.items()}

class RegisteredUser(BaseConverter):
    def to_python(self, value):
        if value in _USERS:
            return _USERS[value]
        raise ValidationError

    def to_url(self, value):
        return _IDS[value]


app = Flask(__name__)
#USE CONVERTERS WITH CARE! KISS!
app.url_map.converters['registered'] = RegisteredUser


#allow for other methods too
#@app.route('/api', methods=['POST', 'DELETE', 'GET'])

#make sure person is of type 'int'
@app.route('/api/person/<registered:name>')

def person(name):
    response = jsonify({'hello':name})
    return response




if __name__ == '__main__':
    print(app.url_map)
    app.run()
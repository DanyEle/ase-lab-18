from flakon import JsonBlueprint
from flask import jsonify, request

calc = JsonBlueprint('calc', __name__)


@calc.route('/calc/sum', methods =['GET'])
def sum():
    m = int(request.args.get('m'))
    n = int(request.args.get('n'))

    result = m + n


    return jsonify({'result':str(result)})

@calc.route('/calc/divide', methods =['GET'])
def divide():
    m = int(request.args.get('m'))
    n = int(request.args.get('n'))

    result = m / n


    return jsonify({'result':str(result)})

@calc.route('/calc/multiply', methods =['GET'])
def multiply():
    m = int(request.args.get('m'))
    n = int(request.args.get('n'))

    result = m * n

    return jsonify({'result':str(result)})

from flask import Flask, jsonify, request
from functools import wraps
from panoptes_aggregation import reducers
from panoptes_aggregation import extractors

application = Flask(__name__, instance_relative_config=True)


def request_wrapper(name):
    def decorator(func):
        @wraps(func)
        def wrapper():
            if request.method == 'GET':
                return name
            else:
                print(name)
                resp = jsonify(func(request))
                resp.status_code = 200
                return resp
        return wrapper
    return decorator


'''
Example use of process_wrapper:
@application.route('/path', method=['POST', 'GET'])
@process_wrapper('string returned on a GET request')
def func(request):
    return

this is the same as:
application.route('/path', methods=['POST', 'GET'])(process_wrapper('string returned on a GET request')(func))
'''


@application.route('/')
def index():
    return 'Python extractors and reducers for panoptes aggregation.'


for route, route_function in reducers.reducers.items():
    application.route('/reducers/{0}'.format(route), methods=['POST', 'GET'])(request_wrapper(route)(route_function))


for route, route_function in extractors.extractors.items():
    application.route('/extractors/{0}'.format(route), methods=['POST', 'GET'])(request_wrapper(route)(route_function))


if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0')

from flask import Flask, jsonify, request
from functools import wraps
import reducers.cluster_points as cp
import reducers

application = Flask(__name__, instance_relative_config=True)


def process_wrapper(name):
    def decorator(func):
        @wraps(func)
        def wrapper():
            if request.method == 'GET':
                return name
            else:
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
    return 'Python reducers for panoptes aggregation.'


for route, route_function in reducers.processes.items():
    application.route('/{0}'.format(route), methods=['POST', 'GET'])(process_wrapper(route)(route_function))


if __name__ == "__main__":
    application.debug = True
    application.run()

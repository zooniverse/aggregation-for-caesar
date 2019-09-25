try:
    from flask import jsonify, request, Flask
    from flask.json import JSONEncoder
    from panoptes_aggregation import panoptes
    import sentry_sdk
    from sentry_sdk.integrations.flask import FlaskIntegration
except ImportError:  # pragma: no cover
    print('You must install `flask` to use panoptes_aggregation.routes')  # pragma: no cover
    raise  # pragma: no cover
from functools import wraps
from os import getenv
from panoptes_aggregation import reducers
from panoptes_aggregation import extractors
from panoptes_aggregation import running_reducers
from panoptes_aggregation import __version__
import numpy as np


class MyEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)


def request_wrapper(name):
    '''
    Example use of process_wrapper:
    @application.route('/path', method=['POST', 'GET'])
    @request_wrapper('string returned on a GET request')
    def func(request):
        return

    this is the same as:
    application.route('/path', methods=['POST', 'GET'])(request_wrapper('string returned on a GET request')(func))
    '''
    def decorator(func):
        @wraps(func)
        def wrapper():
            if request.method == 'GET':
                return jsonify(name)
            else:
                resp = jsonify(func(request))
                resp.status_code = 200
                return resp
        return wrapper
    return decorator


def make_application():
    # setup sentry error reporting with flask integration
    # and the DSN being set via the SENTRY_DSN env var
    # https://docs.sentry.io/error-reporting/configuration/?platform=python#dsn
    sentry_sdk.init(
        request_bodies='always',
        integrations=[FlaskIntegration()]
    )
    # setup the flask app to server web requests
    application = Flask(__name__,
                        instance_relative_config=True,
                        static_url_path='',
                        static_folder='../docs/build/html')
    application.json_encoder = MyEncoder

    home_screen_message = 'Python extractors and reducers for panoptes aggregation. Code version {0}'.format(__version__)

    @application.route('/')
    def index():
        return jsonify(home_screen_message)

    for route, route_function in reducers.reducers.items():
        application.route('/reducers/{0}'.format(route), methods=['POST', 'GET'])(request_wrapper(route)(route_function))

    for route, route_function in extractors.extractors.items():
        application.route('/extractors/{0}'.format(route), methods=['POST', 'GET'])(request_wrapper(route)(route_function))

    for route, route_function in running_reducers.running_reducers.items():
        application.route('/running_reducers/{0}'.format(route), methods=['POST', 'GET'])(request_wrapper(route)(route_function))

    for route, route_function in panoptes.panoptes.items():
        application.route('/panoptes/{0}'.format(route), methods=['POST', 'PUT'])(lambda: route_function(request.args.to_dict(), request.get_json()))

    @application.route('/docs')
    def web_docs():
        return application.send_static_file('index.html')

    return application


if __name__ == "__main__":
    application = make_application()  # pragma: no cover
    application.run(
        debug=True,
        host='0.0.0.0',
        port=getenv('LISTEN_PORT', 80),
    )  # pragma: no cover

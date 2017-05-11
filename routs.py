from flask import Flask, jsonify, request
import reducers.cluster_points as cp

application = Flask(__name__, instance_relative_config=True)


@application.route('/')
def index():
    return 'Python reducers for panoptes aggregation.'


@application.route('/cluster_points', methods=['POST'])
def cluster_points():
    resp = jsonify(cp.process_request(request))
    resp.status_code = 200
    return resp


if __name__ == "__main__":
    application.debug = True
    application.run()

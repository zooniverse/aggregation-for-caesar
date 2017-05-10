from flask import Flask, jsonify, request
import reducers.cluster_points as cp

application = Flask(__name__, instance_relative_config=True)


@application.route('/')
def index():
    return 'It works!'


@application.route('/cluster_points', methods=['POST'])
def cluster_points():
    data = cp.process_data(request.body)
    kwargs = cp.process_kwargs(request.args)
    clusters = cp.cluster_points(data, **kwargs)
    resp = jsonify(clusters)
    resp.status_code = 200
    return resp


if __name__ == "__main__":
    application.debug = True
    application.run()

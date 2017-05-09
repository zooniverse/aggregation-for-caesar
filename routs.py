from flask import Flask, jsonify, request
import reducers.cluster_points as cp

application = Flask(__name__, instance_relative_config=True)


@application.route('/cluster_points/<float:esp>/<int:min_samples>', methods=['POST'])
def cluster_points(esp, min_samples):
    clusters = cp.cluster_points(request.body, esp=esp, min_samples=min_samples)
    resp = jsonify(clusters)
    resp.status_code = 200
    return resp


if __name__ == "__main__":
    application.debug = True
    application.run()

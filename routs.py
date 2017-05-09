from flask import Flask, jsonify, request
import reducers.cluster_points

application = Flask(__name__, instance_relative_config=True)


@application.route('/cluster_points/<float:esp>/<int:min_samples>', methods=['POST'])
def cluster_points(esp, min_samples):
    clusters = reducers.cluster_points(request.body, esp=esp, min_samples=min_samples)
    # write code that POSTs the cluster resutls as json
    return clusters


if __name__ == "__main__":
    application.debug = True
    application.run()

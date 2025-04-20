from flask import Flask, request, jsonify
from plugin import EnergyAwareSchedulerPlugin
import logging

app = Flask(__name__)
plugin = EnergyAwareSchedulerPlugin()

@app.route('/filter', methods=['POST'])
def filter_nodes():
    data = request.get_json()
    node_info = data.get('node_info', {})
    result = plugin.filter(node_info)
    return jsonify({'allowed': result})

@app.route('/score', methods=['POST'])
def score_nodes():
    data = request.get_json()
    node_info = data.get('node_info', {})
    score = plugin.score(node_info)
    return jsonify({'score': score})

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=8080)

from flask import Flask, request, jsonify, Response
from plugin import EnergyAwareSchedulerPlugin
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from energy_aware_scheduler.k8s_plugin.prometheus_exporter import PrometheusExporter
import threading
import logging

app = Flask(__name__)
plugin = EnergyAwareSchedulerPlugin()
exporter = PrometheusExporter(port=8000)

@app.route('/filter', methods=['POST'])
def filter_nodes():
    data = request.get_json()
    node_index = data.get('node_index')
    if node_index is None:
        return jsonify({'error': 'node_index is required'}), 400
    result = plugin.filter(node_index)
    return jsonify({'allowed': result})

@app.route('/score', methods=['POST'])
def score_nodes():
    data = request.get_json()
    node_index = data.get('node_index')
    if node_index is None:
        return jsonify({'error': 'node_index is required'}), 400
    score = plugin.score(node_index)
    return jsonify({'score': score})

@app.route('/metrics')
def metrics():
    data = generate_latest()
    return Response(data, mimetype=CONTENT_TYPE_LATEST)

def start_exporter():
    exporter.start()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    threading.Thread(target=start_exporter, daemon=True).start()
    app.run(host='0.0.0.0', port=8080)

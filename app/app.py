from flask import Flask, render_template
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

REQUEST_COUNT = Counter(
    'flask_request_count',
    'Total request count',
    ['method', 'endpoint']
)

REQUEST_LATENCY = Histogram(
    'flask_request_latency_seconds',
    'Request latency',
    ['endpoint']
)

@app.route('/')
def home():
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    return render_template('index.html')

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

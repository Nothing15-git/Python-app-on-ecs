import os
import time
from flask import Flask, jsonify, request, Response, g
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUESTS = Counter("http_requests_total", "Total HTTP requests", ["method", "path", "status"])
LATENCY = Histogram("http_request_duration_seconds", "Request latency", ["path"])

VERSION = os.getenv("APP_VERSION", "dev")


@app.before_request
def start_timer():
    g.start = time.time()


@app.after_request
def record_metrics(response):
    if request.path != "/metrics":
        LATENCY.labels(request.path).observe(time.time() - g.start)
        REQUESTS.labels(request.method, request.path, response.status_code).inc()
    return response


@app.get("/")
def index():
    return jsonify(message="Hello this is tayyab from the ECS demo app", version=VERSION)


@app.get("/health")
def health():
    return jsonify(status="ok"), 200


@app.get("/api/items")
def items():
    return jsonify(items=[{"id": 1, "name": "alpha"}, {"id": 2, "name": "beta"}])


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

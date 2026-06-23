"""
Sample Flask application for the DevOps practical interview.

Exposes:
  GET /          -> homepage (the line we change for the end-to-end demo)
  GET /healthz   -> liveness/readiness probe target
  GET /metrics   -> Prometheus metrics (request count, latency)
"""
import time
from flask import Flask, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "app_requests_total", "Total HTTP requests", ["method", "endpoint", "status"]
)
REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds", "Request latency", ["endpoint"]
)

HOMEPAGE_TEXT = "Hello from the DevOps Practical Interview app! Version: v1"


@app.before_request
def _start_timer():
    Flask.g_start = time.time()


@app.after_request
def _record_metrics(response):
    endpoint = "unknown"
    try:
        from flask import request
        endpoint = request.path
        latency = time.time() - Flask.g_start
        REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)
        REQUEST_COUNT.labels(
            method=request.method, endpoint=endpoint, status=response.status_code
        ).inc()
    except Exception:
        pass
    return response


@app.route("/")
def home():
    return HOMEPAGE_TEXT, 200


@app.route("/healthz")
def healthz():
    return {"status": "ok"}, 200


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    # 0.0.0.0 so it's reachable inside the container; debug off for prod-like behavior
    app.run(host="0.0.0.0", port=5000)
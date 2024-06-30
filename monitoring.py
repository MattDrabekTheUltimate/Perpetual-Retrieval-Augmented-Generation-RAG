from prometheus_client import start_http_server, Summary, Counter, Gauge

REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
ERROR_COUNT = Counter('error_count', 'Number of errors')
INFERENCE_TIME = Gauge('inference_time_seconds', 'Time spent on model inference')

def start_monitoring_server(port=8000):
    start_http_server(port)
    print(f"Prometheus monitoring server started at http://localhost:{port}")

def track_request_time(func):
    def wrapper(*args, **kwargs):
        with REQUEST_TIME.time():
            return func(*args, **kwargs)
    return wrapper

def increment_error_count():
    ERROR_COUNT.inc()

def track_inference_time(func):
    def wrapper(*args, **kwargs):
        with INFERENCE_TIME.track_inprogress():
            return func(*args, **kwargs)
    return wrapper

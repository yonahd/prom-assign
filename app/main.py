import requests
import prometheus_client as prom
import time
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import logging


URL_LIST = ["https://abc-fake.com", "https://httpstat.us/503", "https://httpstat.us/200"]
URL_STATUS_GAUGE = prom.Gauge('sample_external_url_up', 'This is my gauge', ["url"])
RESPONSE_TIME_GAUGE = prom.Gauge('sample_external_url_response_ms', 'This is my gauge', ["url"])

app = Flask(__name__)

# Add prometheus wsgi middleware to route /metrics requests
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': prom.make_wsgi_app()
})


def get_response(url: str) -> dict:
    response = requests.get(url)
    url_status = 0
    if response.ok is True:
        url_status = 1
    response_time = response.elapsed.total_seconds()
    response_dict = {'status': url_status, 'response_time': response_time}
    return response_dict


def get_url_status():
    while True:
        for url_name in URL_LIST:
            try:
                response = get_response(url_name)
                RESPONSE_TIME_GAUGE.labels(url=url_name).set(response['response_time'])
                URL_STATUS_GAUGE.labels(url=url_name).set(response['status'])
            except requests.exceptions.RequestException as err:
                logging.error(err)
        time.sleep(5)


if __name__ == '__main__':
    prom.start_http_server(80)
    get_url_status()



# prom-app

prom-app is a service that exposes prometheus style metrics for a couple of endpoint.

## Installation

Install helm computer with access to your K8S cluster [helm](https://helm.sh/docs/intro/install/)

```bash
# Current working version 0.1
helm install {app-name} --set image.tag=${VERSION} ./prom-app-helm --set service.type=LoadBalancer
```

### Output

When accessing the service http://IP/metrics the output should look like this

```bash
# HELP sample_external_url_up This is my gauge
# TYPE sample_external_url_up gauge
sample_external_url_up{url="https://httpstat.us/503"} 0.0
sample_external_url_up{url="https://httpstat.us/200"} 1.0
# HELP sample_external_url_response_ms This is my gauge
# TYPE sample_external_url_response_ms gauge
sample_external_url_response_ms{url="https://httpstat.us/503"} 31.85311
sample_external_url_response_ms{url="https://httpstat.us/200"} 64.101549
```

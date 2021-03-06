#!/usr/bin/env python
from prometheus_client import start_http_server, Gauge, Summary
from datetime import datetime
import time
import epetitions as E

# Create a metric to track time spent and requests made.
SIGNATURES = Gauge('signatures',
                   'Number of signatures for this petition', [
                       "id", "name", "created", "status"])
SIG_REQUEST_TIME = Gauge('signature_request_time',
                         'Time this request took to process')


@ SIG_REQUEST_TIME.time()
def get_signatures(include_closed=False):
    params = {}
    if not include_closed:
        params = {"status": "open"}
    sigs = E.get_all(params)
    for sig in sigs:
        sig = E.parse_petition(sig)
        SIGNATURES.labels(
            id=sig.identifier,
            name=sig.label,
            created=datetime.fromisoformat(
                sig.created.replace("Z", "+00:00")).timestamp(),
            status=sig.status).set(
            sig.numberOfSignatures
        )


if __name__ == '__main__':
    # get_signatures()
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    get_signatures(True)
    time.sleep(600)
    while True:
        get_signatures()
        time.sleep(600)

#!/usr/bin/env python
from prometheus_client import start_http_server, Gauge, Summary
from datetime import datetime
import time
import epetitions as E

# Create a metric to track time spent and requests made.
SIGNATURES = Gauge('signatures',
                   'Number of signatures for this petition', [
                       "id", "name", "created"])
SIG_REQUEST_TIME = Summary('signature_request_time',
                           'Time this request took to process')


@ SIG_REQUEST_TIME.time()
def get_signatures():
    sigs = E.get_all()
    for sig in sigs:
        sig = E.parse_petition(sig)
        SIGNATURES.labels(
            id=sig.identifier,
            name=sig.label,
            created=datetime.fromisoformat(sig.created.replace("Z", "+00:00")).timestamp()).set(
            sig.numberOfSignatures
        )


if __name__ == '__main__':
    # get_signatures()
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        get_signatures()
        time.sleep(3600)

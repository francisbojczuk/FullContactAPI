import os

from datetime import datetime, timedelta
import time
import urllib.request, json

class FullContactAdaptiveClient(object):
    REQUEST_LATENCY=0.2
    remaining = 10
    reset = 20

    def __init__(self):
        self.next_req_time = datetime.fromtimestamp( 86400)

    def call_fullcontact(self, email,api_key):
        self._wait_for_rate_limit()
        req = urllib.request.Request('https://api.fullcontact.com/v3/person.enrich')
        req.add_header('Authorization', 'Bearer {}'.format(api_key))
        data = json.dumps({
            "email": "{}".format(email)
        })
        response = urllib.request.urlopen(req, data.encode())
        self._update_rate_limit()
        return response.read()

    def _wait_for_rate_limit(self):
        now = datetime.now()
        if self.next_req_time > now:
            t = self.next_req_time - now
            time.sleep(t.total_seconds())

    def _update_rate_limit(self):
        spacing = reset / (1.0 + remaining)
        delay = spacing - self.REQUEST_LATENCY
        self.next_req_time = datetime.now() + timedelta(seconds=delay)

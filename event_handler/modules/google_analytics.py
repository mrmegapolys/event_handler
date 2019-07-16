import requests
from threading import Lock

class GoogleAnalyticsClient:
    def __init__(self, tracking_id_filepath, verbose=False):
        self._verbose = verbose
        self._print('Authentificating...')
        with open(tracking_id_filepath, 'r') as tid_file:
            self._tracking_id = tid_file.read()[:-1] #the last symbol is '\n'
        self._version = 1
        self.lock = Lock()
        self._print('Authentification successful!')

    def _print(self, *args):
        if self._verbose:
            print("GoogleAnalyticsClient:", *args)

    def _post(self, type_, client_id, state):
        payload = {
            'v': self._version,
            'tid': self._tracking_id,
            'cid': client_id,
            't': type_,
            'dp': state,
        }
        requests.post("http://www.google-analytics.com/collect", data=payload)

    def send_pageview(self, client_id, state):
        self._print('Sending pageview of page \'{}\' by user {}...'.format(state, client_id))
        self._post('pageview', client_id, state)
        self._print('Pageview sent successfully!')

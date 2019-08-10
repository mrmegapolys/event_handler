import requests
import time

class WhatsApp:
    def __init__(self, config):
        self.token = config['token']
        self.endpoint = config['endpoint']
        self.delay = config['polling_delay']
        self.timestamp = time.time()

    def message_emitter(self):
        address = self.endpoint + '/messages'
        params = {
            'token': self.token,
            'last': True,
        }

        while True:
            try:
                response = requests.get(address, params)
                if response.status_code != 200:
                    raise Exception('Bad status code', response.status_code)
                payload = response.json()
                self.timestamp = time.time()
            except Exception as e:
                print(e)

            messages = self._parse_response(payload)
            if messages:
                yield messages
            
    def send_message(self, chat_id, text, markup=None):
        if markup:
            text += self._add_markup(markup)
        params = {
            'phone': chat_id,
            'body': text,
        }
        return self._make_request('sendMessage', params)

    def _make_request(self, method_name, params):
        address = self.endpoint + method_name
        response = requests.post(address,
                                params={'token': self.token},
                                data=params)
        return response.json().get('response')

    def _parse_response(self, response):
        messages = []
        return messages

    @staticmethod
    def _add_markup(markup):
        result = '\n' + '-' * 10 + '\n'
        return result
        
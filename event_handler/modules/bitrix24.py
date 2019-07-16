import requests
from bitrix24 import Bitrix24 as bt24
from datetime import datetime
from threading import Lock


class Bitrix24Client:
    def __init__(self, creds_filepath, tokens_filepath, verbose=False):
        self._verbose = verbose
        self._print('Authentificating...')
        self._tokens_filepath = tokens_filepath
        with open(tokens_filepath, 'r') as f:
            tokens = f.readlines()
        with open(creds_filepath, 'r') as f:
            creds = f.readlines()
        self.lock = Lock()
        self._client = bt24(creds[0][:-1], client_id=creds[1][:-1], client_secret=creds[2][:-1],
                                access_token=tokens[0][:-1], refresh_token=tokens[1][:-1]) #the last symbol is '\n'
        self._refresh_tokens()
        self._print('Authentification successful!')

    def _print(self, *args):
        if self._verbose:
            print("Bitrix24Client:", *args)

    def _refresh_tokens(self):
        self._print('Refreshing tokens...')
        self._client.refresh_tokens()
        tokens = self._client.get_tokens()
        with open(self._tokens_filepath, 'w') as f:
            f.write(tokens['access_token'] + '\n' + tokens['refresh_token'] + '\n')
        self._print('Tokens refreshed!')

    def _make_request(self, method, payload):
        response = self._client.call_method(method, payload)
        if response.get('error') == 'expired_token':
            self._refresh_tokens()
            response = self._client.call_method(method, payload)
        return response

    def add_lead(self, lead_data):
        payload = {'fields': lead_data}
        self._print('Adding new lead...')
        lead_id = self._make_request('crm.lead.add', payload)['result']
        self._print('Lead added successfully, lead id {}'.format(lead_id))
        return lead_id

    def add_contact(self, contact_data):
        payload = {'fields': contact_data} 
        self._print('Adding new contact...')
        contact_id = self._make_request('crm.contact.add', payload)['result']
        self._print('Contact added successfully, contact id {}'.format(contact_id))
        return contact_id

    def get_contact(self, contact_id):
        payload = {'id': contact_id}
        self._print('Retrieving data of contact {}...'.format(contact_id))
        contact_data = self._make_request('crm.contact.get', payload)['result']
        self._print('Data retrieved successfully!')
        return contact_data

    def add_deal(self, deal_data):
        payload = {'fields': deal_data}
        self._print('Adding a new deal...')
        deal_id = self._make_request('crm.deal.add', payload)['result']
        self._print('Deal added successfully, deal id {}'.format(deal_id))
        return deal_id

    def update_deal(self, deal_id, update_data):
        payload = {
            'id': deal_id,
            'fields': update_data
        }
        self._print('Updating deal {}...'.format(deal_id))
        self._make_request('crm.deal.update', payload)
        self._print('Update done successfully!')

    def update_deal_stage(self, deal_id, new_stage):
        update_data = {'STAGE_ID': new_stage}
        self.update_deal(deal_id, update_data)

    def get_deal_list(self, payload=None):
        payload = payload.copy() if payload else {}
        self._print('Retrieving deal list...')
        response = self._make_request('crm.deal.list', payload)
        deal_list = response['result']
        while response.get('next'):
            payload['start'] = response.get('next')
            response = self._make_request('crm.deal.list', payload)
            deal_list.extend(response['result'])
        self._print('Data retrieved successfully!')
        return deal_list

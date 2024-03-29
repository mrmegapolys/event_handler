import requests
from bitrix24 import Bitrix24 as bt24
from datetime import datetime
from threading import Lock
import time

class APIError(Exception):
    def __init__(self, response):
        self.response = response


class Bitrix24:
    def __init__(self, config, verbose=False):
        self._verbose = verbose
        self._print('Authentificating...')
        self.lock = Lock()
        self._client = bt24(config['domain'], client_id=config['client_id'], client_secret=config['client_secret'],
                                access_token=config['access_token'], refresh_token=config['refresh_token'])
        self._client.refresh_tokens()
        self._print('Authentification successful!')

    def _print(self, *args):
        if self._verbose:
            print("Bitrix24Client:", *args)

    def _make_request(self, method, payload):
        while True:
            try:
                response = self._client.call_method(method, payload)
                if not response.get('result'):
                    raise APIError(response)
                return response
            except APIError as e:
                if e.response.get('error') == 'expired_token':
                    try:
                        self._client.refresh_tokens()
                        self._print('Tokens updated!')
                    except Exception as e:
                        print('Token update error:', e)
                else:
                    print('Bitrix24Client: bad response for method \'{}\' with payload {}:'.format(method, payload))
                    print(e.response)
            except Exception as e:
                print('Bitrix24Client: unexpected error:')
                print(e)
            finally:
                time.sleep(1)

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

    def add_commentary(self, message, entity_type_id, entity_id):
        payload = {
            'fields': {
                'MESSAGE': message,
                'ENTITYTYPEID': entity_type_id,
                'ENTITYID': entity_id,
            }
        }
        self._print('Adding commentary with params', payload)
        response = self._make_request('crm.livefeedmessage.add', payload)
        self._print('Commentary added successfully!')
        return response

    def add_msg_to_deal(self, author, text, deal_id):
        message = '{}: {}'.format(author, text)
        entity_type_id = 2 #type id corresponding to deal
        return self.add_commentary(message, entity_type_id, deal_id)

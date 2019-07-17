import gspread
from oauth2client.service_account import ServiceAccountCredentials
from threading import Lock
from functools import wraps

def check_tokens(func):
    @wraps(func)
    def wrapped(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except gspread.exceptions.APIError:
            self._client.login()
            self._print('Tokens updated!')
            return func(self, *args, **kwargs)
    return wrapped


class GoogleSheetsClient:
    def __init__(self, config, verbose=False):
        self._verbose = verbose
        self._print('Authentificating...')
        scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(config['credentials_filepath'], scope)
        self._client = gspread.authorize(creds)
        self.lock = Lock()
        self._print('Authentification successful!')

    def _print(self, *args):
        if self._verbose:
            print("GoogleSheetsClient:", *args)

    @check_tokens
    def open_spreadsheet(self, name_or_url):
        self._print('Opening spreadsheet \'{}\'...'.format(name_or_url))
        if 'docs.google.com' in name_or_url:
            spreadsheet = self._client.open_by_url(name_or_url)
        else:
            spreadsheet = self._client.open(name_or_url)
        self._print('Spreadsheet \'{}\' opened successfully!'.format(name_or_url))
        return spreadsheet

    @check_tokens
    def insert_row(self, worksheet, row, idx):
        self._print("Inserting line {} in worksheet {} at row {}...".format(row, worksheet, idx))
        worksheet.insert_row(row, idx)
        self._print('Insert done!')

    @check_tokens
    def get_all_data(self, worksheet):
        self._print("Retrieving all data from worksheet {}".format(worksheet))
        data =  worksheet.get_all_values()
        self._print("Data retrieved successfully!")
        return data

    @check_tokens
    def get_worksheet_list(self, spreadsheet):
        return spreadsheet.worksheets()


    

    


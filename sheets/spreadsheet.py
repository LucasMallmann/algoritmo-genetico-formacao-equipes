import os
from googleapiclient.discovery import build, Resource
from httplib2 import Http
from oauth2client import file, client, tools
import gspread
from oauth2client.service_account import ServiceAccountCredentials

filepath = os.path.dirname(os.path.realpath(__file__))

def get_client(scopes: list) -> gspread.client.Client:
    # credentials 
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        filepath + '/credentials/tg-result-1540898000261-f1678dec7159.json',
        scopes=scopes
    )
    client = gspread.authorize(credentials)
    return client


def get_connection_service(scopes: list):
    store = file.Storage(filepath + '/credentials/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(filepath + '/credentials/credentials.json', scopes)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    print(type(service))
    return service


class Spreadsheet(object):
    def __init__(self, spreadsheet_id, service):
        self.service = service
        self.spreadsheet_id = spreadsheet_id

    def read(self, range: str):
        '''
        Ler uma planilha passando um range como parâmetro
        '''
        pass



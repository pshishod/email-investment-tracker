import base64
import os.path
import pprint
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class fetchEmail():
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    def __init__(self):
        self.html = []
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        self.service = build('gmail', 'v1', credentials=creds)

    #List all the emails which match the specified query
    def list_messages(self):
        #Query variable will contain the query needed to search through the emails. 
        # This is defined in a query file under the same directory.
        query = ''
        with open('./query') as file:
            for line in file:
                query += line 
        file.close()
        self.message_list = self.service.users().messages().list(userId='me', q=query).execute()
    
    #Get the html from all the emails gotten from the list_messages function. 
    # This method is very specific to current needs, and needs to be modified based on changing needs.
    def get_html(self):
        for i in self.message_list['messages']:
            message = self.service.users().messages().get(userId='me', id=i['id']).execute()
            payload = message['payload']
            for j in payload['parts']:
                if j['mimeType'] == 'text/html':
                    decoded = base64.urlsafe_b64decode(j['body']['data'])
                    decoded = str(decoded, "utf-8")
                    self.html.append(decoded)
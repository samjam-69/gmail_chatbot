from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import base64

# Authenticate with your token and credentials
def bod_met(num):
    creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/gmail.readonly'])
    service = build('gmail', 'v1', credentials=creds)

    # Step 1: Get a list of message IDs
    results = service.users().messages().list(userId='me', maxResults=num).execute()
    messages = results.get('messages', [])
    # Step 2: Loop through messages
    ans=[]
    for msg in messages:
        msg_id = msg['id']
        message = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
        payload=message['payload']
        headers = payload['headers']
        body=''
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    break
                elif part['mimeType'] == 'text/html':
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    break
        else:
            body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
        sender = None
        date = None
        subject = None

        for header in headers:
            if header['name'] == 'From':
                sender = header['value']
            if header['name'] == 'Date':
                date = header['value']
            if header['name'] == 'Subject':
                subject = header['value']
        
        """print("📧 Subject:", subject)
        print("👤 From:", sender)
        print("🕒 Date:", date)
        print(body)
        print("—" * 60)"""
        ans.append({"From":sender,"Subject":subject,"Date":date,'id':msg['id'],'body':body})
    return ans
if __name__=="__main__":
    print(bod_met(1))


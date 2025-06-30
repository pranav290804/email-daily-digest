import os
import base64
import datetime
from email.mime.text import MIMEText

import cohere
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# 🔐 SCOPES
SCOPES = ['https://mail.google.com/']

# 🧠 Cohere setup
COHERE_API_KEY = 'TSh3J5SQMhp8AtJARO64NAp00caBsWPxETHEzR75'
co = cohere.Client(COHERE_API_KEY)
CHUNK_SIZE = 3000  # Max token length to avoid exceeding limits
MAX_EMAILS_PER_CHUNK = 4

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def get_unread_emails(service):
    results = service.users().messages().list(
        userId='me',
        q='is:unread',
        maxResults=100
    ).execute()
    messages = results.get('messages', [])
    email_bodies = []

    if not messages:
        return []

    for msg in messages:
        msg_detail = service.users().messages().get(userId='me', id=msg['id']).execute()
        internal_date = int(msg_detail.get('internalDate', 0)) / 1000
        msg_time = datetime.datetime.utcfromtimestamp(internal_date)

        # Filter emails from last 24 hours
        if msg_time < datetime.datetime.utcnow() - datetime.timedelta(hours=24):
            continue

        payload = msg_detail.get('payload', {})
        headers = payload.get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), '')
        snippet = msg_detail.get('snippet', '')

        email_bodies.append(f"From: {sender}\nSubject: {subject}\nContent: {snippet}")

    return email_bodies


def summarize_emails(email_chunk):
    prompt = "Summarize the following emails into key points with clarity:\n\n"
    prompt += "\n\n---\n\n".join(email_chunk)
    response = co.generate(
        model="command",
        prompt=prompt,
        max_tokens=500,
        temperature=0.4
    )
    return response.generations[0].text.strip()

def send_email(subject, body, service):
    message = MIMEText(body)
    message['to'] = "pranav290804@gmail.com"
    message['from'] = "me"
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {'raw': raw}
    service.users().messages().send(userId='me', body=body).execute()

def main():
    print("🔐 Authenticating...")
    service = authenticate_gmail()

    print("📥 Fetching unread emails from last 24 hours...")
    emails = get_unread_emails(service)
    if not emails:
        print("📭 No unread emails found.")
        return

    print(f"📦 Splitting {len(emails)} emails into manageable chunks...")
    chunks = []
    current_chunk = []
    current_length = 0

    for email in emails:
        if len(current_chunk) >= MAX_EMAILS_PER_CHUNK or current_length + len(email) > CHUNK_SIZE:
            chunks.append(current_chunk)
            current_chunk = [email]
            current_length = len(email)
        else:
            current_chunk.append(email)
            current_length += len(email)

    if current_chunk:
        chunks.append(current_chunk)

    print(f"📚 Total chunks created: {len(chunks)}")

    for i, chunk in enumerate(chunks, 1):
        print(f"🧠 Summarizing chunk {i}...")
        summary = summarize_emails(chunk)
        subject = f"📬 Your Daily Email Digest (Part {i})"
        send_email(subject, summary, service)
        print(f"✅ Sent: {subject}")

if __name__ == '__main__':
    main()

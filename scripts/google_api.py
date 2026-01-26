#!/usr/bin/env python3
"""
Google API Helper Script for Daily Operating System

Handles OAuth authentication and provides CLI interface for Google Calendar and Gmail.

Setup:
    1. Create a Google Cloud project and enable Calendar + Gmail APIs
    2. Create OAuth credentials (Desktop app)
    3. Download credentials.json to this directory
    4. Run: python3 google_api.py auth

Usage:
    python3 google_api.py auth                              # Initial authentication

    # Calendar
    python3 google_api.py calendar list [days]              # List upcoming events
    python3 google_api.py calendar get <id>                 # Get event details
    python3 google_api.py calendar create <title> <start> <end> [desc]  # Create event
    python3 google_api.py calendar delete <id>              # Delete event

    # Gmail
    python3 google_api.py gmail list [max]                  # List recent emails
    python3 google_api.py gmail get <id>                    # Get email content
    python3 google_api.py gmail search <query> [max]        # Search emails
    python3 google_api.py gmail draft <to> <subject> <body> # Create draft
    python3 google_api.py gmail labels list                 # List all labels
    python3 google_api.py gmail labels add <id> <labels>    # Add labels to message
    python3 google_api.py gmail labels remove <id> <labels> # Remove labels
"""

import os
import sys
import json
import base64
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from email.mime.text import MIMEText
except ImportError:
    print("Required packages not installed. Run:")
    print("  pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    sys.exit(1)

# Configuration - files stored in same directory as script
CONFIG_DIR = Path(__file__).parent
CREDENTIALS_FILE = CONFIG_DIR / "credentials.json"
TOKEN_FILE = CONFIG_DIR / "token.json"

# Scopes for Calendar and Gmail
SCOPES = [
    'https://www.googleapis.com/auth/calendar',       # Full calendar access
    'https://www.googleapis.com/auth/gmail.modify',   # Read, modify labels, delete
    'https://www.googleapis.com/auth/gmail.compose',  # Create drafts
]


def get_credentials():
    """Get valid credentials, refreshing or re-authenticating as needed."""
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Token refresh failed: {e}", file=sys.stderr)
                creds = None

        if not creds:
            if not CREDENTIALS_FILE.exists():
                print(f"Error: credentials.json not found at {CREDENTIALS_FILE}", file=sys.stderr)
                print("\nTo set up:")
                print("1. Go to https://console.cloud.google.com/")
                print("2. Create a project and enable Calendar + Gmail APIs")
                print("3. Create OAuth credentials (Desktop app)")
                print("4. Download credentials.json to this directory")
                sys.exit(1)

            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for future runs
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return creds


def cmd_auth():
    """Authenticate and store credentials."""
    print("Starting authentication flow...")
    creds = get_credentials()
    print(f"Authentication successful! Token saved to {TOKEN_FILE}")
    return True


def cmd_calendar_list(days=7):
    """List upcoming calendar events."""
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    end = (datetime.now(timezone.utc) + timedelta(days=int(days))).isoformat().replace('+00:00', 'Z')

    try:
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            timeMax=end,
            maxResults=50,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        if not events:
            print("No upcoming events found.")
            return

        output = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            output.append({
                'id': event['id'],
                'summary': event.get('summary', 'No title'),
                'start': start,
                'end': event['end'].get('dateTime', event['end'].get('date')),
                'location': event.get('location', ''),
                'attendees': [a.get('email') for a in event.get('attendees', [])],
            })

        print(json.dumps(output, indent=2))

    except HttpError as e:
        print(f"Calendar API error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_calendar_get(event_id):
    """Get details of a specific calendar event."""
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    try:
        event = service.events().get(calendarId='primary', eventId=event_id).execute()
        print(json.dumps(event, indent=2))
    except HttpError as e:
        print(f"Calendar API error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_calendar_create(summary, start_time, end_time, description=''):
    """Create a calendar event."""
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    try:
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_time,
                'timeZone': 'America/New_York',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'America/New_York',
            },
        }

        created_event = service.events().insert(calendarId='primary', body=event).execute()

        print(json.dumps({
            'status': 'created',
            'id': created_event['id'],
            'summary': created_event.get('summary'),
            'start': created_event['start'].get('dateTime'),
            'end': created_event['end'].get('dateTime'),
            'htmlLink': created_event.get('htmlLink')
        }, indent=2))

    except HttpError as e:
        print(f"Calendar API error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_calendar_delete(event_id):
    """Delete a calendar event."""
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    try:
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        print(json.dumps({
            'status': 'deleted',
            'id': event_id
        }, indent=2))
    except HttpError as e:
        print(f"Calendar API error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_gmail_list(max_results=20):
    """List recent emails."""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    try:
        results = service.users().messages().list(
            userId='me',
            maxResults=int(max_results),
            labelIds=['INBOX']
        ).execute()
        messages = results.get('messages', [])

        if not messages:
            print("No messages found.")
            return

        output = []
        for msg in messages:
            msg_data = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='metadata',
                metadataHeaders=['From', 'To', 'Subject', 'Date']
            ).execute()

            headers = {h['name']: h['value'] for h in msg_data.get('payload', {}).get('headers', [])}
            output.append({
                'id': msg['id'],
                'threadId': msg['threadId'],
                'snippet': msg_data.get('snippet', ''),
                'from': headers.get('From', ''),
                'to': headers.get('To', ''),
                'subject': headers.get('Subject', ''),
                'date': headers.get('Date', ''),
            })

        print(json.dumps(output, indent=2))

    except HttpError as e:
        print(f"Gmail API error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_gmail_get(message_id):
    """Get full content of an email."""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    try:
        msg = service.users().messages().get(
            userId='me',
            id=message_id,
            format='full'
        ).execute()

        headers = {h['name']: h['value'] for h in msg.get('payload', {}).get('headers', [])}

        # Extract body
        body = ''
        payload = msg.get('payload', {})

        if 'body' in payload and payload['body'].get('data'):
            body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
        elif 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain' and part['body'].get('data'):
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    break

        output = {
            'id': msg['id'],
            'threadId': msg['threadId'],
            'from': headers.get('From', ''),
            'to': headers.get('To', ''),
            'subject': headers.get('Subject', ''),
            'date': headers.get('Date', ''),
            'body': body,
            'labels': msg.get('labelIds', []),
        }

        print(json.dumps(output, indent=2))

    except HttpError as e:
        print(f"Gmail API error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_gmail_draft(to, subject, body):
    """Create a draft email (does not send)."""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    try:
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

        draft = service.users().drafts().create(
            userId='me',
            body={'message': {'raw': raw}}
        ).execute()

        print(json.dumps({
            'status': 'draft_created',
            'id': draft['id'],
            'message_id': draft['message']['id'],
            'note': 'Draft saved. Open Gmail to review and send.'
        }))

    except HttpError as e:
        print(f"Gmail API error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_gmail_search(query, max_results=20):
    """Search emails with Gmail query syntax."""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    try:
        results = service.users().messages().list(
            userId='me',
            maxResults=int(max_results),
            q=query
        ).execute()
        messages = results.get('messages', [])

        if not messages:
            print("No messages found.")
            return

        output = []
        for msg in messages:
            msg_data = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='metadata',
                metadataHeaders=['From', 'To', 'Subject', 'Date']
            ).execute()

            headers = {h['name']: h['value'] for h in msg_data.get('payload', {}).get('headers', [])}
            output.append({
                'id': msg['id'],
                'threadId': msg['threadId'],
                'snippet': msg_data.get('snippet', ''),
                'from': headers.get('From', ''),
                'to': headers.get('To', ''),
                'subject': headers.get('Subject', ''),
                'date': headers.get('Date', ''),
            })

        print(json.dumps(output, indent=2))

    except HttpError as e:
        print(f"Gmail API error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_gmail_labels_list():
    """List all Gmail labels."""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    try:
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        print(json.dumps(labels, indent=2))

    except HttpError as e:
        print(f"Gmail API error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_gmail_labels_add(message_id, label_ids_json):
    """Add labels to a message."""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    try:
        label_ids = json.loads(label_ids_json)
        result = service.users().messages().modify(
            userId='me',
            id=message_id,
            body={'addLabelIds': label_ids}
        ).execute()

        print(json.dumps({
            'status': 'labels_added',
            'messageId': message_id,
            'labelIds': result.get('labelIds')
        }, indent=2))

    except HttpError as e:
        print(f"Gmail API error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_gmail_labels_remove(message_id, label_ids_json):
    """Remove labels from a message."""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    try:
        label_ids = json.loads(label_ids_json)
        result = service.users().messages().modify(
            userId='me',
            id=message_id,
            body={'removeLabelIds': label_ids}
        ).execute()

        print(json.dumps({
            'status': 'labels_removed',
            'messageId': message_id,
            'labelIds': result.get('labelIds')
        }, indent=2))

    except HttpError as e:
        print(f"Gmail API error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == 'auth':
        cmd_auth()

    elif cmd == 'calendar':
        if len(sys.argv) < 3:
            print("Usage: calendar list [days] | get <id> | create <summary> <start> <end> [desc] | delete <id>")
            sys.exit(1)
        subcmd = sys.argv[2]
        if subcmd == 'list':
            days = sys.argv[3] if len(sys.argv) > 3 else 7
            cmd_calendar_list(days)
        elif subcmd == 'get':
            if len(sys.argv) < 4:
                print("Usage: calendar get <event_id>")
                sys.exit(1)
            cmd_calendar_get(sys.argv[3])
        elif subcmd == 'create':
            if len(sys.argv) < 6:
                print("Usage: calendar create <summary> <start_time> <end_time> [description]")
                print("  Times in ISO format: 2026-01-12T09:00:00-05:00")
                sys.exit(1)
            description = sys.argv[6] if len(sys.argv) > 6 else ''
            cmd_calendar_create(sys.argv[3], sys.argv[4], sys.argv[5], description)
        elif subcmd == 'delete':
            if len(sys.argv) < 4:
                print("Usage: calendar delete <event_id>")
                sys.exit(1)
            cmd_calendar_delete(sys.argv[3])
        else:
            print(f"Unknown calendar command: {subcmd}")
            sys.exit(1)

    elif cmd == 'gmail':
        if len(sys.argv) < 3:
            print("Usage: gmail list | get | draft | search | labels")
            sys.exit(1)
        subcmd = sys.argv[2]
        if subcmd == 'list':
            max_results = sys.argv[3] if len(sys.argv) > 3 else 20
            cmd_gmail_list(max_results)
        elif subcmd == 'get':
            if len(sys.argv) < 4:
                print("Usage: gmail get <message_id>")
                sys.exit(1)
            cmd_gmail_get(sys.argv[3])
        elif subcmd == 'draft':
            if len(sys.argv) < 6:
                print("Usage: gmail draft <to> <subject> <body>")
                sys.exit(1)
            cmd_gmail_draft(sys.argv[3], sys.argv[4], sys.argv[5])
        elif subcmd == 'search':
            if len(sys.argv) < 4:
                print("Usage: gmail search <query> [max_results]")
                sys.exit(1)
            max_results = sys.argv[4] if len(sys.argv) > 4 else 20
            cmd_gmail_search(sys.argv[3], max_results)
        elif subcmd == 'labels':
            if len(sys.argv) < 4:
                print("Usage: gmail labels list | add <msg_id> <labels_json> | remove <msg_id> <labels_json>")
                sys.exit(1)
            labels_cmd = sys.argv[3]
            if labels_cmd == 'list':
                cmd_gmail_labels_list()
            elif labels_cmd == 'add':
                if len(sys.argv) < 6:
                    print("Usage: gmail labels add <message_id> '[\"Label1\", \"Label2\"]'")
                    sys.exit(1)
                cmd_gmail_labels_add(sys.argv[4], sys.argv[5])
            elif labels_cmd == 'remove':
                if len(sys.argv) < 6:
                    print("Usage: gmail labels remove <message_id> '[\"Label1\", \"Label2\"]'")
                    sys.exit(1)
                cmd_gmail_labels_remove(sys.argv[4], sys.argv[5])
            else:
                print(f"Unknown labels command: {labels_cmd}")
                sys.exit(1)
        else:
            print(f"Unknown gmail command: {subcmd}")
            sys.exit(1)

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == '__main__':
    main()

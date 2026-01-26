# Google API Setup Reference

Detailed reference for the `google_api.py` helper script.

## Available Commands

### Authentication

```bash
python3 google_api.py auth
```

Initiates OAuth flow and saves credentials.

### Calendar

```bash
# List upcoming events (default: 7 days)
python3 google_api.py calendar list [days]

# Get specific event details
python3 google_api.py calendar get <event_id>

# Create an event
python3 google_api.py calendar create <title> <start> <end> [description]
# Times in ISO format: 2026-01-12T09:00:00-05:00

# Delete an event
python3 google_api.py calendar delete <event_id>
```

### Gmail

```bash
# List recent emails
python3 google_api.py gmail list [max_results]

# Get full email content
python3 google_api.py gmail get <message_id>

# Search emails (Gmail query syntax)
python3 google_api.py gmail search <query> [max_results]

# Create a draft (does not send)
python3 google_api.py gmail draft <to> <subject> <body>

# List all labels
python3 google_api.py gmail labels list

# Add labels to a message
python3 google_api.py gmail labels add <message_id> '["Label1"]'

# Remove labels (e.g., archive by removing INBOX)
python3 google_api.py gmail labels remove <message_id> '["INBOX"]'
```

## Output Format

All commands output JSON for easy parsing:

```json
{
  "id": "event123",
  "summary": "Team Meeting",
  "start": "2026-01-20T10:00:00-05:00",
  "end": "2026-01-20T11:00:00-05:00",
  "attendees": ["alice@company.com", "bob@company.com"]
}
```

## Gmail Query Syntax

Common search operators:

| Query | Matches |
|-------|---------|
| `is:unread` | Unread messages |
| `in:inbox` | Messages in inbox |
| `from:email@example.com` | From specific sender |
| `to:email@example.com` | To specific recipient |
| `subject:keyword` | Subject contains keyword |
| `has:attachment` | Has attachments |
| `after:2026/01/01` | After date |
| `before:2026/01/31` | Before date |
| `newer_than:7d` | Last 7 days |

Combine with spaces: `is:unread in:inbox from:client@example.com`

## Required Scopes

The script requests these OAuth scopes:

- `calendar` - Full calendar access (read/write)
- `gmail.modify` - Read, modify labels, delete messages
- `gmail.compose` - Create drafts (cannot send)

## File Locations

| File | Purpose |
|------|---------|
| `credentials.json` | OAuth client configuration (from Google Cloud) |
| `token.json` | Your access token (auto-generated) |

Both files should be in the `scripts/` directory and are gitignored.

## Error Codes

| Error | Cause | Solution |
|-------|-------|----------|
| `credentials.json not found` | Missing OAuth config | Download from Google Cloud Console |
| `Token refresh failed` | Expired/revoked token | Delete token.json and re-auth |
| `HttpError 403` | Permission denied | Check scopes, re-auth |
| `HttpError 404` | Resource not found | Check event/message ID |

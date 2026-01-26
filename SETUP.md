# Setup Guide

This guide walks through setting up the Daily Operating System skill, including Google API integration for calendar and email.

## Quick Setup (No Google API)

If you don't want to set up Google API, you can still use the skill with manual meeting entry:

1. Run `/today --setup`
2. When asked about calendar, choose "manual"
3. When asked about email, choose "no"
4. Each morning, you'll be prompted to enter your meetings

This still gives you meeting prep files, action item tracking, and focus suggestions—just without automatic calendar/email integration.

---

## Full Setup (With Google API)

### Prerequisites

- Python 3.8 or higher
- A Google account
- ~15 minutes for initial setup

### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name it something like "Daily OS" and create it
4. Select your new project

### Step 2: Enable APIs

1. Go to "APIs & Services" → "Library"
2. Search for and enable each:
   - **Google Calendar API**
   - **Gmail API** (if you want email integration)

### Step 3: Configure OAuth Consent Screen

1. Go to "APIs & Services" → "OAuth consent screen"
2. Choose "External" (unless you have a Google Workspace org)
3. Fill in required fields:
   - App name: "Daily OS"
   - User support email: your email
   - Developer contact: your email
4. Click "Save and Continue"
5. On Scopes page, click "Add or Remove Scopes"
6. Add these scopes:
   - `https://www.googleapis.com/auth/calendar` (Calendar full access)
   - `https://www.googleapis.com/auth/gmail.modify` (Gmail read/modify)
   - `https://www.googleapis.com/auth/gmail.compose` (Gmail drafts)
7. Save and continue through remaining screens
8. Add your email as a test user

### Step 4: Create Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Application type: "Desktop app"
4. Name: "Daily OS CLI"
5. Click "Create"
6. Click "Download JSON"
7. Save as `credentials.json` in the skill's `scripts/` folder

### Step 5: Install Python Dependencies

```bash
cd ~/.claude/skills/daily-operating-system/scripts

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Step 6: Authenticate

```bash
python3 google_api.py auth
```

This will:
1. Open a browser window
2. Ask you to sign in to Google
3. Ask you to grant permissions
4. Save a token locally for future use

You should see: "Authentication successful!"

### Step 7: Test It

```bash
# Test calendar
python3 google_api.py calendar list 1

# Test email (if enabled)
python3 google_api.py gmail list 5
```

### Step 8: Configure the Skill

Run `/today --setup` and:
1. Enter your internal email domains
2. Optionally specify a customer folder path
3. Confirm Google Calendar is configured
4. Choose whether to enable email integration

---

## Troubleshooting

### "credentials.json not found"

Make sure `credentials.json` is in the `scripts/` folder, not the root folder.

### "Token refresh failed"

Delete `token.json` and run `python3 google_api.py auth` again.

### "Access blocked: This app's request is invalid"

Your OAuth consent screen may not be configured correctly. Go back to the consent screen setup and make sure:
- You've added your email as a test user
- The required scopes are added

### "Permission denied" errors

The token may have expired or been revoked. Delete `token.json` and re-authenticate.

### Calendar shows no events

Make sure:
- You're checking the right calendar (defaults to primary)
- Events exist in the time range being queried
- The Calendar API is enabled in Google Cloud Console

---

## Security Notes

- `credentials.json` contains your OAuth client secret—don't commit it to git
- `token.json` contains your access token—don't share it
- Both files are in `.gitignore` by default
- The script only requests the permissions it needs
- Gmail integration can create drafts but cannot send emails directly

---

## Manual Calendar Entry

If you don't want to set up Google API, the skill will prompt you for meetings:

```
What meetings do you have today?

Enter each meeting in this format:
TIME | TITLE | ATTENDEES (comma-separated emails)

Example:
9:00 | Team Standup | alice@company.com, bob@company.com
14:00 | Client Call | contact@client.com

Enter 'done' when finished.
```

This is less convenient but still gives you the full meeting prep workflow.

---

## Updating Permissions

If you need to add or change API permissions later:

1. Delete `token.json`
2. Update the `SCOPES` list in `google_api.py` if needed
3. Run `python3 google_api.py auth` again
4. Grant the new permissions

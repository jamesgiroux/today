# Setup Guide

This guide helps you set up the Daily Operating System skill. But before diving into the mechanics, let's think through what will make this work well for you.

## Before You Start: Think About Your File System

This skill works best when you have **local files that contain context about the people and projects you meet about**. It doesn't require a specific structure, but having *some* structure helps.

### The Ideal Setup

The skill shines when you have something like:

```
Your-Work-Folder/
├── Accounts/           # or Customers/, Clients/, Projects/
│   ├── Acme-Corp/
│   │   ├── meeting-notes/
│   │   ├── action-items.md
│   │   └── context.md
│   ├── Big-Client/
│   └── Partner-Co/
├── _today/             # Created by this skill
└── ... your other stuff
```

When you have a meeting with someone from Acme Corp, the skill can pull context from `Accounts/Acme-Corp/` and include it in your prep.

### What If I Don't Have This?

That's fine. The skill still works. You'll get:
- Meeting prep files for every meeting
- Action items from any task files you do have
- Email triage (if enabled)
- A daily overview

You just won't get the "pull context from customer folder" magic. Many people start here and gradually build up their file structure as they see the value.

### What If My Structure Is Different?

The skill is flexible. During setup, you'll specify:
- **Your internal email domains** - So it knows which meetings are internal vs external
- **Your customer folder path** (optional) - Where to look for context

It matches external attendee email domains to folder names. `jane@acme.com` → looks for `Acme/` or `Acme-Corp/` folder.

---

## Setup Options

You have two paths:

### Path A: Full Setup (Calendar + Email) — Recommended

Takes ~15-20 minutes. You'll configure Google Calendar and Gmail APIs. This gives you:
- Automatic calendar reading
- Email triage and prioritization
- The full experience

### Path B: Calendar Only

Takes ~10-15 minutes. Just Google Calendar API. You'll get:
- Automatic calendar reading
- Meeting prep files
- Action items and focus suggestions
- No email integration

### Path C: Manual Mode

No API setup required. You'll manually enter your meetings each morning. Useful if:
- You can't set up Google API (work restrictions, etc.)
- You want to try the skill before committing to setup
- Your calendar is in a system without API access

---

## Path A: Full Setup with Google APIs

### Step 1: Create a Google Cloud Project

This is where you'll configure API access. It sounds intimidating but takes about 5 minutes.

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name it something like "Daily OS" or "Personal Productivity"
4. Click "Create" and wait a few seconds
5. Make sure your new project is selected

### Step 2: Enable the APIs

1. In the left sidebar, go to "APIs & Services" → "Library"
2. Search for **Google Calendar API** and click "Enable"
3. Search for **Gmail API** and click "Enable"

### Step 3: Configure OAuth Consent Screen

This tells Google what your app does when it asks for permissions.

1. Go to "APIs & Services" → "OAuth consent screen"
2. Select **External** (unless you have a Google Workspace org and want Internal)
3. Fill in the required fields:
   - **App name**: "Daily OS" (or whatever you want)
   - **User support email**: Your email
   - **Developer contact**: Your email
4. Click "Save and Continue"
5. On the **Scopes** page:
   - Click "Add or Remove Scopes"
   - Add these scopes:
     - `https://www.googleapis.com/auth/calendar`
     - `https://www.googleapis.com/auth/gmail.modify`
     - `https://www.googleapis.com/auth/gmail.compose`
   - Click "Update" then "Save and Continue"
6. On the **Test users** page:
   - Click "Add Users"
   - Add your own email address
   - Click "Save and Continue"
7. Review and click "Back to Dashboard"

**Why test users?** Until you "publish" your app (unnecessary for personal use), only test users can authenticate. Adding yourself is all you need.

### Step 4: Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Application type: **Desktop app**
4. Name: "Daily OS CLI" (or whatever)
5. Click "Create"
6. Click "Download JSON" on the popup
7. **Important**: Save this file as `credentials.json` in the skill's `scripts/` folder:
   ```
   ~/.claude/skills/daily-operating-system/scripts/credentials.json
   ```

### Step 5: Install Python Dependencies

The Google API requires a few Python packages:

```bash
cd ~/.claude/skills/daily-operating-system/scripts

# Option A: Use a virtual environment (cleaner)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client

# Option B: Install globally (simpler)
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Step 6: Authenticate

```bash
python3 google_api.py auth
```

This will:
1. Open your browser
2. Ask you to sign in to Google
3. Show the permissions being requested (Calendar and Gmail access)
4. Ask you to grant access

After you approve, you'll see: `Authentication successful!`

A `token.json` file is created—this stores your access token so you don't have to re-authenticate every time.

### Step 7: Test It

```bash
# Test calendar access
python3 google_api.py calendar list 1

# Test email access
python3 google_api.py gmail list 5
```

You should see JSON output with your upcoming events and recent emails.

### Step 8: Run Skill Setup

Now run the skill's setup wizard:

```
/today --setup
```

This will ask you about:
- Your internal email domains (e.g., `@yourcompany.com`)
- Where you keep customer/account context (optional)
- Confirm that Calendar is configured
- Whether to enable email integration

---

## Path B: Calendar Only

Follow Steps 1-7 above, but:
- In Step 2, only enable Google Calendar API
- In Step 3, only add the calendar scope
- When running `/today --setup`, say "no" to email integration

---

## Path C: Manual Mode

No Google API setup needed.

1. Run `/today --setup`
2. When asked about calendar, choose "manual"
3. When asked about email, choose "no"

Each morning when you run `/today`, you'll be prompted to enter your meetings:

```
What meetings do you have today?

Enter each meeting as: TIME | TITLE | ATTENDEES
Example: 10:00 | Acme Sync | jane@acme.com, bob@acme.com

Type 'done' when finished.
```

This still gives you meeting prep files and the daily structure—just without automatic calendar reading.

---

## After Setup

### Your First /today

Run `/today` and check the `_today/` folder in your working directory:

- `00-overview.md` - Your daily dashboard
- Individual meeting prep files
- `80-actions-due.md` - Action items (if you have task files)
- `83-email-summary.md` - Email triage (if enabled)

### Building the Habit

The skill works best as a **morning ritual**:

1. Open Claude Code
2. Run `/today`
3. Review `00-overview.md`
4. Open prep files before meetings

After a few days, you'll wonder how you worked without it.

### Evolving Your File Structure

As you use the skill, you may want to create or improve your customer/project folders. The prep files become much more useful when there's context to pull from.

A simple structure to start:

```
Accounts/
├── Customer-Name/
│   ├── notes.md           # Running notes from meetings
│   └── actions.md         # Open action items
```

The skill will find and include this context automatically.

---

## Troubleshooting

### "credentials.json not found"

Make sure the file is in the `scripts/` folder, not the root folder of the skill.

### "Token refresh failed"

Your token expired or was revoked. Delete `token.json` and run `python3 google_api.py auth` again.

### "Access blocked: This app's request is invalid"

The OAuth consent screen isn't configured correctly. Check:
- You've added yourself as a test user
- The required scopes are added

### Calendar shows no events

- Make sure events exist in the time range (today)
- Check you're looking at the right calendar (defaults to primary)
- Verify the Calendar API is enabled in Google Cloud Console

### Email shows no results

- Check your Gmail has unread messages in the inbox
- Verify the Gmail API is enabled
- Make sure both gmail scopes were added to the consent screen

---

## Security Notes

Your credentials and tokens are stored locally:

| File | Contents | Keep Private |
|------|----------|--------------|
| `credentials.json` | OAuth client configuration | Yes |
| `token.json` | Your access token | Yes |

Both are in `.gitignore` by default. Never commit them to a public repo.

The skill can:
- **Read** your calendar and email
- **Create** calendar events and email drafts
- **Cannot** send emails directly (only creates drafts)

---

## Updating Permissions

If you need to change what the skill can access:

1. Delete `token.json`
2. Update scopes in `google_api.py` if needed
3. Update scopes in Google Cloud Console
4. Run `python3 google_api.py auth` again
5. Grant the new permissions

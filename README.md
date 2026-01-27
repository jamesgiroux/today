# Daily Operating System

A Claude Code skill that prepares you for every meeting on your calendar.

```bash
npx skills add jamesgiroux/daily-operating-system
```

## What It Does

`/today` runs once each morning. It looks at your calendar, your files, your email, and assembles everything you need for the day ahead:

- Meeting prep files for every meeting, with extra context for customer calls
- Action items surfaced by due date (overdue, due today, coming up)
- Email triage showing what needs attention vs. noise
- Focus suggestions for gaps between meetings

## Who This Is For

This skill works best if you:

- Have recurring meetings with the same people (customers, partners, stakeholders)
- Keep notes and context in local files or folders
- Use Google Calendar (required) and optionally Gmail
- Want to start each day knowing what's ahead instead of discovering it in real-time

Particularly valuable for account managers, consultants, managers running 1:1s, or anyone with meeting-heavy days where continuity matters.

## How It Works

When you run `/today`:

1. Archives yesterday's files to `_today/archive/`
2. Pulls today's meetings from Google Calendar
3. Classifies each meeting as customer, internal, or personal based on attendee domains
4. Generates a prep file for each meeting, with depth based on type
5. Scans email (optional) to surface high-priority items
6. Aggregates action items from your task files, organized by due date
7. Creates your daily overview

Output structure:
```
_today/
├── 00-overview.md              # Your daily dashboard
├── 01-0900-standup.md          # Meeting at 9am
├── 02-1000-customer-acme.md    # Customer meeting with full context
├── 03-1400-partner-sync.md     # External meeting
├── 80-actions-due.md           # Action items by due date
├── 81-suggested-focus.md       # What to work on between meetings
├── 83-email-summary.md         # Email triage (if enabled)
└── archive/                    # Previous days
```

## Quick Start

1. Run `/today --setup` to configure internal email domains and customer folder path
2. Set up Google Calendar API (~15 min). See [SETUP.md](SETUP.md).
3. Run `/today` each morning
4. Check `_today/00-overview.md` for your daily dashboard

## Requirements

- Claude Code
- Python 3.8+ (for Google API integration)
- Google Calendar API (required)
- Gmail API (optional, for email triage)

## Configuration

After running `/today --setup`, your config lives at `_today/config.yaml`:

```yaml
internal_domains:
  - "@yourcompany.com"

customer_folder: "Accounts"  # Where you keep customer context (or null)

integrations:
  calendar:
    enabled: true
    provider: "google"
  email:
    enabled: false  # Set to true if you configured Gmail
```

## Learn More

- [SETUP.md](SETUP.md) - Detailed setup guide including Google API configuration
- [references/](references/) - How meeting classification and email triage work

## License

MIT

## Contributing

This started as a personal system I've refined over months of daily use. Issues and PRs welcome, especially for making setup easier or extending the meeting classification logic.

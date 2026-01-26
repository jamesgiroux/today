# Daily Operating System

A Claude Code skill that prepares your workday automatically. Run `/today` each morning to get meeting prep, action items, email triage, and focus areas—all in one place.

## What It Does

- **Meeting Prep**: Creates context files for each meeting, with extra detail for customer/external calls
- **Action Items**: Surfaces what's due today, what's overdue, and what's coming up
- **Email Triage**: Scans your inbox and highlights what needs attention (optional, requires Gmail API)
- **Focus Areas**: Suggests what to work on during downtime
- **Auto-Archive**: Yesterday's files get archived automatically

## Installation

```bash
npx skills add yourusername/daily-operating-system
```

Or clone directly:

```bash
git clone https://github.com/yourusername/daily-operating-system.git ~/.claude/skills/daily-operating-system
```

## Quick Start

1. **Run setup** (first time only):
   ```
   /today --setup
   ```

2. **Run daily** (each morning):
   ```
   /today
   ```

3. **Check your `_today/` folder** for:
   - `00-overview.md` - Your daily dashboard
   - Meeting prep files numbered by time
   - `80-actions-due.md` - Action items
   - `83-email-summary.md` - Email summary (if enabled)

## Setup Options

During setup, you'll configure:

| Option | Required | Description |
|--------|----------|-------------|
| Internal domains | Yes | Email domains for your org (e.g., `@company.com`) |
| Customer folder | No | Path to customer/account context (e.g., `Accounts/`) |
| Calendar | Yes | Google Calendar API or manual entry |
| Email | No | Gmail API for inbox triage |

## Google API Setup

For calendar and email integration, you'll need to set up Google API credentials. See [SETUP.md](SETUP.md) for detailed instructions.

**Quick version:**
1. Create a Google Cloud project
2. Enable Calendar and Gmail APIs
3. Create OAuth credentials
4. Download `credentials.json` to `scripts/`
5. Run `python3 scripts/google_api.py auth`

## File Structure

After running `/today`:

```
_today/
├── 00-overview.md              # Daily dashboard
├── 01-0900-meeting-name.md     # Meeting prep (by time)
├── 02-1100-team-sync.md
├── 03-1400-customer-call.md    # Customer meetings get extra context
├── 80-actions-due.md           # Action items
├── 81-suggested-focus.md       # Focus areas
├── 83-email-summary.md         # Email triage
├── tasks/
│   └── master-task-list.md     # Persistent task list
├── config.yaml                 # Your configuration
└── archive/
    └── 2026-01-20/             # Yesterday's files
```

## Configuration

Your config lives at `_today/config.yaml`:

```yaml
internal_domains:
  - "@company.com"
  - "@corp.company.com"

customer_folder: "Accounts"  # or null

integrations:
  calendar:
    enabled: true
    provider: "google"
  email:
    enabled: true
    provider: "google"

archive_days: 7
```

## How Meeting Classification Works

| Attendees | Classification | Prep Level |
|-----------|---------------|------------|
| None or only you | Personal | Minimal |
| All internal domains | Internal | Minimal |
| External + matches customer folder | Customer | Full prep with context |
| External + no match | External | Basic with attendee list |

## Customization

### Add More Internal Domains

Edit `_today/config.yaml`:

```yaml
internal_domains:
  - "@company.com"
  - "@subsidiary.com"
  - "@contractor.company.com"
```

### Change Customer Folder Location

```yaml
customer_folder: "Clients"  # or "Customers", "Accounts", etc.
```

### Disable Email Integration

```yaml
integrations:
  email:
    enabled: false
```

## Requirements

- Claude Code
- Python 3.8+ (for Google API script)
- Google API credentials (for calendar/email integration)

## License

MIT

## Contributing

Issues and PRs welcome. This started as a personal productivity system and is being shared in the spirit of "what works for me might work for you."

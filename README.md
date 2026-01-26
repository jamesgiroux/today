# Daily Operating System

**A Claude Code skill that eliminates the "what do I need to know before this meeting?" scramble.**

## The Problem

Every knowledge worker knows this moment: You're five minutes from a meeting. You know you talked to this person last month. There were action items. Maybe an email thread? You scramble through Slack, your notes app, your calendar, your inbox—trying to reconstruct context that should have been at your fingertips.

Or worse: You walk into the meeting cold. You ask questions they already answered. You forget the commitment you made. You look unprepared because you *were* unprepared.

This isn't a character flaw. It's a systems problem.

**Your context is scattered across twelve apps. No single tool knows what you need to know before each meeting.**

## The Solution

`/today` runs once each morning. It looks at your calendar, your files, your email, and assembles everything you need for the day ahead:

- **Meeting prep files** for every meeting, with extra context for customer/external calls
- **Action items** surfaced by due date—what's overdue, what's due today, what's coming
- **Email triage** showing what actually needs attention vs. what's noise
- **Focus suggestions** for the gaps between meetings

By the time you finish your coffee, you know what your day looks like and what you need to be ready for.

## What a Morning Looks Like

**Before /today:**
```
8:45 AM - Open calendar. See "Acme Corp Sync" at 10am.
8:46 AM - What did we talk about last time? Search notes...
8:52 AM - Found it. Were there action items? Check task app...
8:58 AM - Did they email me about something? Search inbox...
9:04 AM - What's their current status again? Check CRM...
9:15 AM - Give up. Wing it.
```

**After /today:**
```
8:45 AM - Run /today
8:46 AM - Open _today/00-overview.md
8:47 AM - See Acme meeting at 10am with prep link
8:48 AM - Open prep file. Context, recent history, open actions, suggested topics.
8:49 AM - Ready.
```

The difference isn't magic. It's having a system that assembles context *before* you need it.

## Who This Is For

This skill works best if you:

- Have **recurring meetings** with the same people (customers, partners, stakeholders)
- Keep **notes and context** in local files or folders
- Use **Google Calendar** (required) and optionally **Gmail**
- Want to **start each day knowing what's ahead** instead of discovering it in real-time

It's particularly valuable for:
- **Account managers and customer success** - Every customer call benefits from context
- **Consultants** - Multiple clients, each with their own history
- **Managers** - 1:1s and team meetings where continuity matters
- **Anyone with meeting-heavy days** - Reduce the cognitive load of context-switching

## What It Actually Does

When you run `/today`:

1. **Archives yesterday** - Previous day's files move to `_today/archive/`
2. **Reads your calendar** - Pulls today's meetings from Google Calendar
3. **Classifies each meeting** - Customer, internal, or personal based on attendee domains
4. **Generates prep files** - One file per meeting, with depth based on type
5. **Scans email** (optional) - Surfaces high-priority items, counts the rest
6. **Aggregates action items** - From your task files, organized by due date
7. **Creates your daily overview** - Single file showing the full picture

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

## Installation

```bash
npx skills add jamesgiroux/daily-operating-system
```

Or clone directly:
```bash
git clone https://github.com/jamesgiroux/daily-operating-system.git ~/.claude/skills/daily-operating-system
```

## Quick Start

1. **Run setup**:
   ```
   /today --setup
   ```
   This walks you through configuration—internal email domains, where you keep customer context, and whether to enable email integration.

2. **Configure Google Calendar** (required):
   See [SETUP.md](SETUP.md) for the ~15 minute OAuth setup.

3. **Run daily**:
   ```
   /today
   ```

4. **Check `_today/00-overview.md`** for your daily dashboard.

## The Philosophy

This isn't about automating your job. It's about **eliminating the friction between you and the context you need**.

Every minute spent hunting for "what did we discuss last time?" is a minute not spent on the actual work. Every meeting entered without context is a relationship slightly degraded.

The best systems don't require discipline—they make the right thing the easy thing. `/today` makes being prepared the default.

## Requirements

- **Claude Code**
- **Python 3.8+** (for Google API integration)
- **Google Calendar API** (required)
- **Gmail API** (optional, for email triage)

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

This started as a personal system that I've refined over months of daily use. Issues and PRs welcome—especially if you find ways to make setup easier or extend the meeting classification logic.

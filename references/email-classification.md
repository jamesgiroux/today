# Email Classification Reference

How the skill classifies and triages emails.

## Priority Levels

### HIGH Priority

Emails that need your attention today.

**Criteria (any match):**
- From a domain matching your customer folder
- Subject contains action words: "urgent", "asap", "action required", "please review"
- From leadership/executives (if patterns defined)
- Reply requested with deadline

**Action:** Surface in daily overview with full summary.

### MEDIUM Priority

Emails to be aware of but not urgent.

**Criteria:**
- From internal colleagues
- Meeting-related (invites, updates, declines)
- P2/internal notification systems
- CC'd rather than direct recipient

**Action:** Count in summary, available for review.

### LOW Priority

Noise that can be safely ignored or auto-archived.

**Criteria:**
- Newsletters and marketing
- Automated notifications (CI/CD, GitHub without @mention)
- Calendar confirmations
- Out-of-office auto-replies

**Action:** Can be auto-archived or ignored.

## Classification Logic

```python
def classify_email(email, config):
    sender = email.get('from', '')
    subject = email.get('subject', '').lower()

    # Check HIGH priority patterns
    customer_domains = get_customer_domains(config.get('customer_folder'))
    if any(domain in sender for domain in customer_domains):
        return 'HIGH'

    action_words = ['urgent', 'asap', 'action required', 'please review',
                    'deadline', 'eod', 'end of day', 'by tomorrow']
    if any(word in subject for word in action_words):
        return 'HIGH'

    # Check MEDIUM priority patterns
    internal_domains = config.get('internal_domains', [])
    if any(domain in sender for domain in internal_domains):
        return 'MEDIUM'

    if 'meeting' in subject or 'invite' in subject:
        return 'MEDIUM'

    # Default to LOW
    return 'LOW'
```

## Email Summary Format

The skill generates `83-email-summary.md`:

```markdown
# Email Summary - January 20, 2026

## High Priority (3)

| From | Subject | Type | Notes |
|------|---------|------|-------|
| client@acme.com | Re: Project timeline | CUSTOMER | Asking about delivery date |
| boss@company.com | Please review proposal | ACTION | Review requested by EOD |
| vip@partner.org | Urgent: Contract question | URGENT | Needs response |

## Summary
- **High priority**: 3 emails need attention
- **Medium priority**: 12 emails (internal, meetings)
- **Low priority**: 28 emails (newsletters, automated)

## Suggested Actions
- [ ] Reply to Acme re: timeline
- [ ] Review proposal for boss
- [ ] Respond to partner contract question
```

## Customizing Classification

You can adjust classification by modifying patterns in your workflow:

### Add High-Priority Senders

Track specific senders as always high priority:

```yaml
# In your notes or config
high_priority_senders:
  - "ceo@company.com"
  - "important-client@customer.com"
```

### Add Action Keywords

Expand the list of action-triggering words:

```python
action_words = [
    'urgent', 'asap', 'action required',
    'please review', 'deadline', 'eod',
    'blocker', 'critical', 'p0', 'p1'
]
```

### Domain-Based Rules

Classify by sender domain patterns:

| Domain Pattern | Classification | Reason |
|----------------|---------------|--------|
| `*@customer.com` | HIGH | Customer communication |
| `*@company.com` | MEDIUM | Internal |
| `*@github.com` | LOW | Automated notifications |
| `*@newsletter.*` | LOW | Marketing |

## Integration with Meetings

When a HIGH priority email is from someone you're meeting with today:

1. Email context gets added to meeting prep
2. Flagged in daily overview
3. Suggested talking point: "Follow up on [subject] email"

This ensures you don't walk into a meeting unaware of recent communication.

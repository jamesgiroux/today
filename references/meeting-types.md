# Meeting Classification Reference

How the skill classifies meetings and determines prep level.

## Classification Flow

```
1. Check attendees list
   ├── No attendees or only you → PERSONAL
   │
   ├── All attendees match internal domains → INTERNAL
   │
   └── External attendees present
       ├── Domain matches customer folder → CUSTOMER
       └── Domain doesn't match → EXTERNAL
```

## Meeting Types

### PERSONAL

**Definition:** No attendees, or only you as the attendee.

**Examples:**
- Focus time blocks
- "Deep work" calendar holds
- Personal appointments
- Lunch blocks

**Prep generated:** Minimal placeholder

```markdown
# Focus Time
**9:00 AM - 11:00 AM | Personal**

## Notes

```

### INTERNAL

**Definition:** All attendees are from internal domains.

**Examples:**
- Team standups
- 1:1s with colleagues
- Department meetings
- All-hands

**Prep generated:** Basic structure with attendee list

```markdown
# Weekly Team Sync
**10:00 AM | Internal**

## Attendees
- alice@company.com
- bob@company.com
- carol@company.com

## Notes

```

### CUSTOMER

**Definition:** External attendees whose domain matches a folder in your customer directory.

**Examples:**
- Client calls
- Account reviews
- Customer onboarding sessions
- Support escalations

**Prep generated:** Full prep with context

```markdown
# Acme Corp Monthly Review
**2:00 PM | Customer**

## Attendees
- john@acme.com - VP Engineering
- jane@acme.com - Project Manager

## Recent Context
*(From Accounts/Acme/)*

Last meeting (Jan 15): Discussed Q1 roadmap...

## Open Action Items
- [ ] Send updated timeline - Due Jan 22

## Discussion Topics
1. Follow up on roadmap feedback
2. Review open support tickets

## Notes

```

### EXTERNAL

**Definition:** External attendees whose domain doesn't match any customer folder.

**Examples:**
- Vendor demos
- Partner introductions
- Recruitment calls
- Unknown external meetings

**Prep generated:** Basic with attendee context

```markdown
# Demo: New Vendor Tool
**3:00 PM | External**

## Attendees
- sales@vendor.io - Sales Rep
- demo@vendor.io - Solutions Engineer

## Company
vendor.io (unknown - no existing relationship found)

## Notes

```

## Domain Matching

### Internal Domains

Configured in `_today/config.yaml`:

```yaml
internal_domains:
  - "@company.com"
  - "@corp.company.com"
  - "@subsidiary.com"
```

All variations of your organization's email domains.

### Customer Domain Matching

The skill looks for folders in your customer directory that might match the external domain:

```python
def find_customer_folder(domain, customer_path):
    """
    Try to match email domain to customer folder.

    Examples:
    - acme.com → Accounts/Acme/
    - big-corp.io → Accounts/Big-Corp/
    """
    # Remove TLD, normalize
    company_name = domain.split('.')[0]

    # Look for matching folder (case-insensitive)
    for folder in list_folders(customer_path):
        if folder.lower() == company_name.lower():
            return folder
        if company_name.lower() in folder.lower():
            return folder

    return None
```

### Manual Overrides

For complex cases (conglomerates, subsidiaries), you can maintain a domain mapping:

```yaml
# Optional: domain_mapping.yaml
salesforce.com: Salesforce
appexchange.salesforce.com: Salesforce
heroku.com: Salesforce
```

## Prep Depth by Type

| Type | Attendees | Context Lookup | Action Items | Suggested Topics |
|------|-----------|----------------|--------------|------------------|
| Personal | - | - | - | - |
| Internal | Yes | - | - | - |
| External | Yes | Basic | - | - |
| Customer | Yes | Full | Yes | Yes |

## Edge Cases

### Mixed Internal/External

If a meeting has both internal and external attendees, classify based on external:
- External matches customer → CUSTOMER
- External doesn't match → EXTERNAL

### Unknown Domains

If an external domain isn't recognized:
1. Classify as EXTERNAL
2. Note the domain for future reference
3. After the meeting, consider adding to customer folder if relationship established

### Multiple Customers

Rare case: attendees from multiple customer domains.
- Generate prep for primary customer (first external attendee)
- Note other customers in prep file

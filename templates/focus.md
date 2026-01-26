# Suggested Focus - {{date}}

## Priority 1: Pre-Meeting Prep

{{#if meetingPrep}}
{{#each meetingPrep}}
- [ ] Review {{customer}} prep before {{time}} call
{{/each}}
{{else}}
No customer meetings today requiring prep review.
{{/if}}

## Priority 2: Overdue Items

{{#if overdueItems}}
{{#each overdueItems}}
- [ ] Address: {{action}} ({{daysOverdue}} days overdue)
{{/each}}
{{else}}
No overdue items.
{{/if}}

## Priority 3: Follow-ups

{{#if followUps}}
{{#each followUps}}
- [ ] {{action}}
{{/each}}
{{else}}
No immediate follow-ups identified.
{{/if}}

## If Time Available

{{#if lowPriority}}
{{#each lowPriority}}
- [ ] {{action}}
{{/each}}
{{else}}
- [ ] Review and organize recent notes
- [ ] Update task list
- [ ] Clear email backlog
{{/if}}

---

## Energy-Aware Notes

| Time Block | Energy Level | Best For |
|------------|--------------|----------|
| Morning | High | Strategic work, customer calls, complex problems |
| After lunch | Medium | Meetings, collaboration, reviews |
| Late afternoon | Lower | Admin tasks, email, planning tomorrow |

*Adapt based on your personal energy patterns.*

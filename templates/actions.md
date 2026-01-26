# Action Items - {{date}}

## Overdue

{{#if overdueItems}}
{{#each overdueItems}}
- [ ] **{{action}}** - Due: {{dueDate}} ({{daysOverdue}} days overdue)
  - Source: {{source}}
{{/each}}
{{else}}
(none)
{{/if}}

## Due Today

{{#if todayItems}}
{{#each todayItems}}
- [ ] **{{action}}**
  - Source: {{source}}
{{/each}}
{{else}}
(none)
{{/if}}

{{#if meetingRelatedItems}}
## Related to Today's Meetings

{{#each meetingRelatedItems}}
### {{meetingName}} ({{meetingTime}})
{{#each items}}
- [ ] {{action}}
{{/each}}

{{/each}}
{{/if}}

## Due This Week

{{#if weekItems}}
{{#each weekItems}}
- [ ] **{{action}}** - Due: {{dueDate}}
  - Source: {{source}}
{{/each}}
{{else}}
(none)
{{/if}}

## Upcoming (Next 2 Weeks)

{{#if upcomingItems}}
{{#each upcomingItems}}
- [ ] **{{action}}** - Due: {{dueDate}}
{{/each}}
{{else}}
(none)
{{/if}}

---

*Aggregated from task files at {{generatedAt}}*

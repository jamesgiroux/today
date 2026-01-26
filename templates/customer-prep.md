# {{customerName}} Meeting Prep
**{{time}} | {{title}}**

## Attendees
{{#each attendees}}
- {{email}}{{#if role}} - {{role}}{{/if}}
{{/each}}

## Recent Context
*(From: {{customerFolder}})*

{{#if recentContext}}
{{recentContext}}
{{else}}
No recent meeting notes found. Check {{customerFolder}} for context.
{{/if}}

## Open Action Items
{{#if actionItems}}
{{#each actionItems}}
- [ ] **{{action}}**{{#if dueDate}} - Due: {{dueDate}}{{/if}}
  - Source: {{source}}
{{/each}}
{{else}}
No open action items found.
{{/if}}

## Discussion Topics
{{#if suggestedTopics}}
{{#each suggestedTopics}}
{{@index}}. {{this}}
{{/each}}
{{else}}
1. Check in on recent work
2. Discuss upcoming priorities
3. Surface any blockers
{{/if}}

## Questions to Ask
- What's top of mind for you this week?
- Any blockers we should discuss?
- How can I help?

## Notes


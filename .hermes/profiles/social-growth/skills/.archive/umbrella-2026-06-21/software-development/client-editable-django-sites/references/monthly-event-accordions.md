# Monthly Event Accordions for PTA/Community Calendars

Use when a parent/community event page is becoming a long scroll. The UX goal is cognitive ease: parents should see the current month first and only open older/future months when needed.

## Pattern

- Query published events in normal date order.
- Group by `(event.date.year, event.date.month)` in an ordered mapping.
- For each group expose:
  - `key`: stable `YYYY-MM` string
  - `label`: `Month YYYY`
  - `events`: events in that month
  - `is_past`: group month before current local month
  - `is_current`: group month equals current local month
  - `is_open`: current month first; otherwise first future month; otherwise most recent past month
- Render groups as `<details>` / `<summary>` accordions for accessible native behavior.
- Keep past months collapsed by default; do not delete them unless the user wants archival pruning.
- On mobile, make `summary` a large tap target and put detail buttons full-width.
- Optional JS: when one panel opens, close sibling panels for app-like one-open-month behavior.

## Django view sketch

```python
from collections import OrderedDict
from django.utils import timezone

def events(request):
    category = request.GET.get('category')
    qs = Event.objects.filter(published=True)
    if category:
        qs = qs.filter(category=category)

    today = timezone.localdate()
    current_key = (today.year, today.month)
    grouped = OrderedDict()
    for event in qs:
        key = (event.date.year, event.date.month)
        grouped.setdefault(key, {
            'key': f'{event.date.year}-{event.date.month:02d}',
            'label': event.date.strftime('%B %Y'),
            'events': [],
            'is_past': key < current_key,
            'is_current': key == current_key,
        })['events'].append(event)

    open_key = None
    if current_key in grouped:
        open_key = grouped[current_key]['key']
    else:
        future = [g for key, g in grouped.items() if key > current_key]
        open_key = future[0]['key'] if future else (next(reversed(grouped.values()))['key'] if grouped else None)

    event_months = []
    for group in grouped.values():
        group['is_open'] = group['key'] == open_key
        event_months.append(group)
```

## Template sketch

```django
<div class="events-accordion" data-accordion="events">
  {% for month in event_months %}
  <details class="event-month {% if month.is_past %}past-month{% endif %}" {% if month.is_open %}open{% endif %}>
    <summary>
      <span>{{ month.label }}</span>
      <span>{% if month.is_current %}This month{% elif month.is_past %}Past{% else %}Upcoming{% endif %} · {{ month.events|length }} event{{ month.events|length|pluralize }}</span>
    </summary>
    {% for event in month.events %}
      <!-- event card -->
    {% endfor %}
  </details>
  {% endfor %}
</div>
```

## Test assertions

- Response contains `events-accordion`.
- Current, past, and future month labels render for seeded events.
- Current group has `is_open=True` when current-month events exist.
- Past group has `is_open=False`.
- If no current-month events exist, first future month has `is_open=True`.

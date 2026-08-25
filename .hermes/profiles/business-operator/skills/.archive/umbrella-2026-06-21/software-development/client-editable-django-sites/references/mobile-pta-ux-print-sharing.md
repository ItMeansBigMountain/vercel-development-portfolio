# Mobile PTA UX, Print Sharing, and Announcement Patterns

Use this reference when improving school/PTA/community Django sites that are edited through admin and used heavily by parents on phones.

## Public wording

- Prefer user-facing labels like **Newsletter**, **Update**, or **Post** over **Issue** when the audience could read “issue” as “problem.”
- Internal Django model names can remain stable if migration churn is not worth it; set `verbose_name` / `verbose_name_plural` and template copy instead.

## Volunteer form dropdowns

Django `ModelChoiceField` shows `---------` by default for non-required or blank choices. On public forms this looks broken.

Pattern:

```python
class VolunteerInterestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field = self.fields["opportunity"]
        field.empty_label = None
        if field.queryset.exists():
            field.initial = field.queryset.first()
        else:
            field.required = False
            field.widget = forms.HiddenInput()
```

Test both cases: when an opportunity exists, no `---------`; when none exist, no visible empty select.

## Flyer/newsletter detail layout

For uploaded flyers/newsletters, parents usually need to read or screenshot the image. Use:

```text
[large image/flyer]
[text summary + buttons]
```

Avoid side-by-side desktop layouts unless the image is secondary. Mobile should always stack image first.

## QR + printable pages

For announcements/flyers, create:

- normal web detail page: `/announcements/<id>/`
- print page: `/announcements/<id>/print/`

Print page includes:

- flyer/image
- short explanatory text
- QR code pointing to the web/detail URL or print URL
- print button hidden by `@media print`
- `@media print` CSS hiding nav/footer/actions

Quick QR option for prototypes:

```html
<img src="https://quickchart.io/qr?size=240&margin=2&text={{ request.build_absolute_uri|urlencode }}" alt="QR code">
```

For privacy-sensitive or mission-critical deployments, generate QR codes server-side or pin a reliable QR provider.

## Motion and consumer psychology

- Homepage is the conversion surface: place timely announcements and primary CTAs before archival content.
- Navy = official/trustworthy primary action. Gold = high-attention warmth. Soft blue/white = breathing room and safety.
- Use motion sparingly: reveal-on-scroll, gentle icon bob, CTA shine, tap feedback. Respect `prefers-reduced-motion`.
- Mobile app feel: 56px+ tap targets, full-width key buttons, rounded inputs/cards, strong focus states, bottom-friendly spacing, no tiny text.

## Tests to add

- public volunteer form does not contain `---------`
- newsletter page says `Read newsletter`, not `Read issue`
- announcement detail and print URLs return 200 and contain QR markup
- mobile/print CSS exists if templates expose print buttons

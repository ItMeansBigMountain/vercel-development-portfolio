# Denver-area sperm donor application notes

## Fairfax multi-location intake

- The Fairfax/BeASpermDonor registration page may have Denver-oriented marketing context while the actual location selector omits Denver.
- Observed branch choices included Austin, Fairfax, Houston, Philadelphia, Roseville, Pasadena, Miami, Chicago, and Las Vegas.
- Verify the live selector before entering or submitting account details. If Denver is absent, do not substitute another city without the user's choice.
- The location selector is a Material UI combobox. When click does not expose options, focus `[role="combobox"]`, press Space, inspect `[role="option"]`, select, and verify the resulting text/value.

## Official Denver alternative

- Denver Sperm Bank: https://www.denverspermbank.com/
- Public contact: donor@denverspermbank.com, (303) 970-5897.
- Public office address observed: 1601 East 19th Ave, Suite 4500, Denver, CO 80218.
- Public overview advertised compensation up to $10,000/year and listed age 21–39, healthy, student/young professional, legally able to work in the U.S., and approximately 1–5 hours/month. Re-check live wording because eligibility and compensation can change.

## Intake quirks

- The first application is one long Gravity Form, not a short account-registration page.
- Required topics observed: contact/address, age, height, weight, hair/eye color, education/enrollment, employment, maternal and paternal ancestry, adoption/family-history availability, biological children, recent infectious disease, discovery source, and referral-code status.
- The phone field disclosed that supplying a phone number authorizes phone/text communication. Surface this before submission when the user has said they do not want reminders; reminder preference and intake contact consent are not necessarily equivalent.
- Inspect `.gfield` containers and map visible text to child control IDs to recover exact labels and conditional fields.
- Prefill only known identity/contact details. Collect medical, ancestry, education, employment, and address answers directly from the user, and obtain explicit confirmation immediately before Submit.

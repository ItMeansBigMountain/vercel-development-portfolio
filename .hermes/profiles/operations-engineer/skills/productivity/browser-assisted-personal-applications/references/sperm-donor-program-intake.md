# Sperm Donor Program Intake: Chicago Suburbs Pattern

Session-derived public notes for future browser-assisted application work. Do not store personal applicant answers here.

## Search pattern

- Start broad with: `sperm donor application <city/suburb> <state> sperm bank`.
- If the user corrects location mid-turn, pivot immediately and search the corrected suburb/metro.
- Distinguish donor/applicant pages from recipient/patient pages. Many fertility-clinic results describe using donor sperm, not becoming a donor.

## Chicago/Bloomingdale example

For a user near Bloomingdale, IL, the closer credible donor-program result found was:

- **Midwest Sperm Bank** — 4333 Main Street, Downers Grove, IL 60515
- Public contact shown: `msbdg2@gmail.com`, `(630) 810-0217`
- Public donor application/intake URL: `https://www.midwestspermbank.com/donor-information-request-form/`

A fallback/metro option found was:

- **Fairfax Cryobank Chicago** — `https://beaspermdonor.com/office/chicago/`
- Contact shown: `ChicagoDonors@fairfaxcryobank.com`
- Notes: downtown Chicago/Loop; donation hours may show as "Coming Soon" on the page; initial compact form asks first name, last name, email.

## Midwest Sperm Bank form fields observed

The Downers Grove donor information request form exposed these fields via input placeholders/names:

1. Email Address
2. Cell Phone Number
3. First Name
4. Last Name
5. City, State (where you currently live)
6. Date of Birth
7. Height
8. Weight
9. Hair color
10. Eye Color
11. Brief personal medical history/background
12. Brief education, occupation, citizenship, and anything else applicant wants to add
13. Will you be in the area for the next 12 to 18 months?
14. Do you reside or work close enough to visit twice a week?
15. Are you able to donate at least once a week?

## Public eligibility criteria observed for Midwest Sperm Bank

- In Chicagoland area
- Able to commit 12–18 months / year-and-a-half program
- Reliable transportation
- U.S. citizen, proof required
- Illinois resident
- At least 5'10" tall
- Between 21 and 40 years old
- Sexual partners exclusively female
- Attending a four-year university or already holds a bachelor's/advanced degree
- In good health

## Fairfax Cryobank multi-step application pattern

The official Fairfax donor portal at `https://beaspermdonor.com/application/step/registration` exposes six stages:

1. Create Account
2. Initial Information
3. Your Medical Profile
4. Your Personal Profile
5. Essay
6. Donor Profile Items

The registration page fields observed were legal first name, optional middle name, legal last name, location selector, phone number, phone confirmation, email address, password, and a required yes/no choice for SMS reminders. The location selector is a custom Material UI combobox rather than a native `<select>`. A normal click may appear to do nothing: focus `[role="combobox"]`, press `Space`, then inspect the rendered listbox/options.

In the July 2026 portal check, the live application options were Austin, Fairfax, Houston, Philadelphia, Roseville, Pasadena, Miami, Chicago, and Las Vegas; **Denver was not offered**, despite separate Fairfax web pages mentioning Denver-area recipient/fertility services. This list may change, so always inspect it live. Never promise or select a requested branch until it appears in the applicant portal. If absent, leave location unset and ask whether to choose an offered branch or find a different local donor program.

Work page-by-page: collect and fill registration fields first, create the account only with explicit permission, then inspect each later page before asking for medical/personal answers. Treat account creation as a submission checkpoint and the completed application as a separate final submission checkpoint. Recommend a new site-unique password rather than requesting an existing credential, and never retain or quote it.

## Practical lessons

- When the application link button does not navigate visibly, inspect anchors and navigate directly to the discovered href.
- For sensitive medical/fertility forms, summarize criteria and exact field list, then ask for the user's data and explicit submit confirmation.

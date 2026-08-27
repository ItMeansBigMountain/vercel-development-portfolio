YT: Viral Radar priority; route Classical Echos→Sosai Oyama→A F. Daily Stoic→A F, one video/email; description top: Daily Stoic/Ryan Holiday/Robert Greene affiliate offers + disclosure. Delete email+media only after verified upload; failures backlog by Gmail ID, retain email for remake.
§
User has five Google Workspace email profiles: personal-main (primary personal), personal-secondary (backup/restricted), hermes-agent (Hermes automation/account-linked communications), burner (temporary/disposable sending), classicalechos (archive/curated content sending). Faceless YouTube channel processes fareed320 newsletters (TLDR/Daily Stoic/Kino) into daily videos, with cleanup and email deletion post-upload.
§
User wants Agentic Robinhood auto-trading: monitor/manage cron, high deployment; Venice/redteam pentest.
§
Google Workspace policy: affan.fareed@gmail.com and fareed320@gmail.com have user-approved full read/write Workspace permissions, incl. Gmail read/modify/send.
§
google-workspace skill expects credentials at /opt/data/google_token.json and /opt/data/google_client_secret.json, but user's multi-profile setup stores tokens at /opt/data/google_profiles/<profile>/. Fix: copy verified personal-main profile creds to root Hermes location for skill compatibility.
§
User prefers direct console URLs for Google Cloud actions — no digging through menus. Provide exact project-scoped URLs (e.g., https://console.cloud.google.com/iam-admin/iam?project=hermes-user-oauth).
§
Faceless YouTube pipeline (Daily Stoic → A F) was paused with stale backlog (23 preflight JSONs Aug 16-23 + pending upload queue). User directed: clear stale inventory (B) and park pipeline (C) — completed, job c9e81ae638fe paused.
§
User's OAuth client project is 'hermes-user-oauth' (client_id: 984335329962-jmsnmsu79o45n751hdguq832dqool860.apps.googleusercontent.com), NOT the 'Hermes' project (airy-sled-497503-r8). Service account creation requires IAM roles in hermes-user-oauth project.
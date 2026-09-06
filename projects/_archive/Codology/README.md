# Codology

## Overview
Codology is a lightweight kid-friendly coding review game for the **Basic 13** algorithm drills. Players start immediately, review Python and JavaScript code cards, answer multiple-choice questions, then enter their name after the game to submit their score/time to the leaderboard.

## Live URLs
- **Frontend:** https://codology-three.vercel.app
- **Latest deployment:** https://codology-ky38h3a53-itmeansbigmountains-projects.vercel.app
- **API highscores:** https://codology-api.vercel.app/api/highscores

## Source
- **Remote URL:** https://github.com/ItMeansBigMountain/Codology.git
- **Default Branch:** main

## Current Functionality
- No login/signup required in the frontend flow.
- Home screen starts the quiz directly.
- The quiz covers all 13 Basic 13 drills in both Python and JavaScript.
- Broken image/logo questions were replaced with reliable styled **Code Picture** cards, so the visual prompt is rendered text instead of missing assets.
- Each card includes a kid-friendly tip explaining the coding idea.
- End-of-game screen collects a display name.
- Scores are submitted anonymously to `/api/add-highscore`.
- Leaderboard screen fetches and renders `/api/highscores`.
- API sorts leaderboard rows by highest score, then fastest time.

## Basic 13 Coverage
1. Print all numbers 1 - 255
2. Print all odd numbers 1 - 255
3. Print the sum of all numbers 1 - 255
4. Print all values in an array
5. Print maximum value in an array
6. Print the average of an array
7. Push all odd numbers from 1 - 255 into an array
8. Square all values in an array
9. Print all items greater than 10 within an array
10. Convert all odd items into zero within an array
11. Print maximum, minimum, and average of an array
12. Shift all values of an array to the left, making the last item the first item
13. Convert all negative items into the string `"below zero"`

## Data / Database Note
Codology does **not** need a user database for the current product shape because there are no user accounts. The deployed API currently uses demo-mode in-memory highscores when no database environment variable is configured. That is fine for a live demo, but scores are not guaranteed to survive Vercel cold starts/redeploys.

If a durable global leaderboard becomes important later, add a small persistent store such as Vercel KV/Redis, Supabase, Neon/Postgres, or another hosted database. That still would not require user accounts unless we decide to add real profiles.

## Development
```bash
# Source checks for no-login leaderboard flow and Basic 13 content
npm test

# Export web frontend
cd codology
npx expo export --platform web
```

## Recent Notes
- Replaced missing/broken question images with code-card visuals.
- Added 26 Basic 13 questions: 13 Python and 13 JavaScript.
- Removed login from the app flow.
- Reworked the game ending so players type their name only after completing a round.
- Redeployed frontend to Vercel alias `codology-three.vercel.app`.
- Redeployed API to Vercel alias `codology-api.vercel.app`.

const assert = require('assert');
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const app = fs.readFileSync(path.join(root, 'codology', 'App.js'), 'utf8');
const home = fs.readFileSync(path.join(root, 'codology', 'screens', 'HomeScreen.js'), 'utf8');
const highscore = fs.readFileSync(path.join(root, 'codology', 'screens', 'HighScoreScreen.js'), 'utf8');

function assertDoesNotMatch(text, regex, message) {
  assert(!regex.test(text), message);
}

assertDoesNotMatch(app, /LoginScreen|name=["']Login["']/, 'App should not import or render the login screen');
assert.match(app, /initialRouteName=["']Home["']|<Stack\.Screen\s+name=["']Home["']/, 'App should route directly to Home');

assert.match(home, /TextInput/, 'Home should let the player enter a display name after the game');
assert.match(home, /playerName|displayName|leaderboardName/i, 'Home should track the player name for leaderboard submission');
assert.match(home, /isGameOver|gameOver|showNameEntry/i, 'Home should have a post-game state before leaderboard submission');
assert.match(home, /add-highscore/, 'Home should submit score/time/name to the highscore API');
assert.match(home, /navigation\.navigate\(['"]HighScores['"]\)|navigation\.replace\(['"]HighScores['"]\)/, 'Home should navigate to the leaderboard after submitting');
assertDoesNotMatch(home, /username:\s*["']sosai["']/, 'Home should not submit a hard-coded username');

assert.match(highscore, /setHighscores|highscores/i, 'HighScoreScreen should keep fetched leaderboard rows in state');
assert.match(highscore, /map\(/, 'HighScoreScreen should render leaderboard rows, not only log them');

console.log('no-login leaderboard flow source checks passed');

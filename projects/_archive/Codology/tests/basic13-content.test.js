const assert = require('assert');
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const home = fs.readFileSync(path.join(root, 'codology', 'screens', 'HomeScreen.js'), 'utf8');
const questionsPath = path.join(root, 'codology', 'data', 'basic13Questions.js');
assert(fs.existsSync(questionsPath), 'Basic 13 questions should live in codology/data/basic13Questions.js');
const questions = fs.readFileSync(questionsPath, 'utf8');

function count(regex, text) {
  return (text.match(regex) || []).length;
}

assert(!/import\s+\{[^}]*\bImage\b|<Image\b|require\(['"]\.\.\/assets\//.test(home), 'Home should not depend on missing/static picture assets for questions');
assert.match(home, /codeSnippet|codeCard|Code Picture|codeVisual/i, 'Home should render code as a reliable visual card instead of broken pictures');

for (let i = 1; i <= 13; i += 1) {
  const id = `basic-${i}`;
  assert(questions.includes(id), `Missing Basic 13 challenge id ${id}`);
}

assert(count(/language:\s*['"]Python['"]/g, questions) >= 13, 'Should include at least one Python question for every Basic 13 challenge');
assert(count(/language:\s*['"]JavaScript['"]/g, questions) >= 13, 'Should include at least one JavaScript question for every Basic 13 challenge');
assert(count(/kidTip:/g, questions) >= 26, 'Every Python and JavaScript question should include a kid-friendly learning tip');

[
  'print numbers 1 - 255',
  'print odd numbers 1 - 255',
  'sum of all numbers 1 - 255',
  'print all values in an array',
  'maximum value',
  'average',
  'push all odd numbers',
  'square all values',
  'greater than 10',
  'odd items into zero',
  'maximum, minimum, and average',
  'shift all values',
  'below zero',
].forEach((phrase) => {
  assert(questions.toLowerCase().includes(phrase), `Missing kid-facing Basic 13 phrase: ${phrase}`);
});

console.log('Basic 13 quiz content checks passed');

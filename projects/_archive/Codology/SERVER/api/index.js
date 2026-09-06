const express = require('express');
const cors = require('cors');
const { signup, login, isAuth } = require('../auth.js');
const { addHighScore, displayHighScores } = require('../highscore.js');

const app = express();
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(cors());

app.use((_, res, next) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    next();
});

// Routes
app.get('/api/highscores', displayHighScores);
app.post('/api/add-highscore', addHighScore);
app.post('/api/login', login);
app.post('/api/signup', signup);
app.get('/api/private', isAuth);
app.get('/api/public', (_, res) => {
    res.status(200).json({ message: "here is your public resource" });
});

app.use('/', (_, res) => {
    res.status(404).json({ error: "page not found" });
});

module.exports = app;
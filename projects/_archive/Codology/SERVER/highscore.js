// highscore.js
const { DataTypes } = require('sequelize');
const sequelize = require('./database');
const { hasConfiguredDatabase } = require('./database');
const User = require('./user.js');

const demoHighscores = [];

// HIGHSCORES SQL MODEL
const Highscore = sequelize.define('highscores', {
    username: {
        type: DataTypes.STRING,
        allowNull: false,
    },
    score: {
        type: DataTypes.INTEGER,
        allowNull: false,
    },
    time: {
        type: DataTypes.INTEGER,
        allowNull: false,
    },
    timestamp: {
        type: DataTypes.DATE,
        defaultValue: DataTypes.NOW,
    },
});

const addHighScore = async (req, res) => {
    try {
        const entry = {
            username: req.body.username || 'player',
            score: Number(req.body.score || 0),
            time: Number(req.body.time || 0),
            timestamp: req.body.timestamp || new Date().toISOString(),
        };

        if (!hasConfiguredDatabase) {
            demoHighscores.push(entry);
            demoHighscores.sort((a, b) => b.score - a.score || a.time - b.time);
            return res.status(200).json({ message: 'successful post', demoMode: true });
        }

        // CHECK IF USER IN DATABASE
        const dbUser = await User.findOne({ where: { username: entry.username } });
        if (!dbUser) return res.status(404).json({ message: 'user not found' });

        await Highscore.create(entry);
        return res.status(200).json({ message: 'successful post' });
    } catch (error) {
        console.error('highscore error:', error);
        return res.status(500).json({ message: 'internal server error' });
    }
};

const displayHighScores = async (_req, res) => {
    try {
        if (!hasConfiguredDatabase) {
            return res.status(200).json({ highscores: demoHighscores, demoMode: true });
        }
        const highscores = await Highscore.findAll({ order: [['score', 'DESC'], ['time', 'ASC']] });
        return res.status(200).json({ highscores });
    } catch (error) {
        console.error('highscore list error:', error);
        return res.status(500).json({ message: 'internal server error' });
    }
};

module.exports = { Highscore, addHighScore, displayHighScores };

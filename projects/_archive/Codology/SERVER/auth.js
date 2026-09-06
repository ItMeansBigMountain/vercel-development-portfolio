const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const User = require('./user.js');
const { hasConfiguredDatabase } = require('./database.js');

const JWT_SECRET = process.env.JWT_SECRET || 'codology-demo-secret';
const demoUsers = new Map();

const publicUser = (body) => ({
    email: body.email,
    username: body.username || (body.email ? body.email.split('@')[0] : 'player'),
});

const issueToken = (user) => jwt.sign(
    { email: user.email, username: user.username },
    JWT_SECRET,
    { expiresIn: '7d' }
);

const demoSignup = async (req, res) => {
    const { email, password } = req.body || {};
    if (!password) return res.status(400).json({ message: 'password not provided' });
    if (!email) return res.status(400).json({ message: 'email not provided' });

    const user = publicUser(req.body);
    demoUsers.set(email.toLowerCase(), { ...user, password });
    return res.status(200).json({
        message: 'user created',
        token: issueToken(user),
        demoMode: true,
    });
};

const demoLogin = async (req, res) => {
    const { email, password } = req.body || {};
    if (!password) return res.status(400).json({ message: 'password not provided' });
    if (!email) return res.status(400).json({ message: 'email not provided' });

    const user = demoUsers.get(email.toLowerCase()) || publicUser(req.body);
    return res.status(200).json({
        message: 'user logged in',
        token: issueToken(user),
        demoMode: true,
    });
};

const signup = async (req, res) => {
    if (!hasConfiguredDatabase) return demoSignup(req, res);

    try {
        const dbUser = await User.findOne({ where: { email: req.body.email } });
        if (dbUser) return res.status(409).json({ message: 'email already exists' });
        if (!req.body.password) return res.status(400).json({ message: 'password not provided' });
        if (!req.body.email) return res.status(400).json({ message: 'email not provided' });

        const passwordHash = await bcrypt.hash(req.body.password, 12);
        const created = await User.create({
            email: req.body.email,
            password: passwordHash,
            first_name: req.body.firstname,
            last_name: req.body.lastname,
            phone_number: req.body.phonenumber,
            username: req.body.username || req.body.email.split('@')[0],
        });

        const token = issueToken(created);
        return res.status(200).json({ message: 'user created', token });
    } catch (err) {
        console.error('signup error', err);
        return res.status(502).json({ message: 'error while creating the user' });
    }
};

const login = async (req, res) => {
    if (!hasConfiguredDatabase) return demoLogin(req, res);

    try {
        const dbUser = await User.findOne({ where: { email: req.body.email } });
        if (!dbUser) return res.status(404).json({ message: 'user not found' });

        const compareRes = await bcrypt.compare(req.body.password, dbUser.password);
        if (!compareRes) return res.status(401).json({ message: 'invalid credentials' });

        const token = issueToken(dbUser);
        return res.status(200).json({ message: 'user logged in', token });
    } catch (err) {
        console.error('login error', err);
        return res.status(502).json({ message: 'error while checking user credentials' });
    }
};

const isAuth = (req, res) => {
    const authHeader = req.get('Authorization');
    if (!authHeader) return res.status(401).json({ message: 'not authenticated' });

    const token = authHeader.split(' ')[1];
    try {
        jwt.verify(token, JWT_SECRET);
        return res.status(200).json({ message: 'here is your resource' });
    } catch (err) {
        return res.status(401).json({ message: err.message || 'could not decode the token' });
    }
};

module.exports = { signup, login, isAuth };

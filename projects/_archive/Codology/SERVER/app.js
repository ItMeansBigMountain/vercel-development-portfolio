const express = require('express');
const sequelize = require('./database.js')
const router = require('./routes.js')
const cors = require('cors');



// INIT
const app = express();
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use((_, res, next) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    next();
});


// CORS
app.use(cors());


// API ENDPOINTS
app.use(router);


// PORT NUMBER
sequelize.sync(); 
app.listen(5000, '0.0.0.0');
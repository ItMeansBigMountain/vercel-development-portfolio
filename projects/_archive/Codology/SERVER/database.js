const { Sequelize } = require('sequelize');
const mysql2 = require('mysql2');

const databaseUrl = process.env.DATABASE_URL || process.env.MYSQL_URL;
const hasConfiguredDatabase = Boolean(databaseUrl || process.env.MYSQL_HOST);

const sequelize = databaseUrl
    ? new Sequelize(databaseUrl, {
        dialect: 'mysql',
        dialectModule: mysql2,
        logging: false,
        pool: { acquire: 3000 },
    })
    : new Sequelize(
        process.env.MYSQL_DATABASE || 'Codology',
        process.env.MYSQL_USER || 'root',
        process.env.MYSQL_PASSWORD || 'YOUR_DB_PASSWORD',
        {
            dialect: 'mysql',
            dialectModule: mysql2,
            host: process.env.MYSQL_HOST || 'localhost',
            logging: false,
            pool: { acquire: 3000 },
        }
    );

module.exports = sequelize;
module.exports.hasConfiguredDatabase = hasConfiguredDatabase;

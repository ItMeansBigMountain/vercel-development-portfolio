const { Sequelize } = require('sequelize');
const sequelize = require('./database.js');

const User = sequelize.define('users', {
    id: {
        type: Sequelize.INTEGER,
        autoIncrement: true,
        allowNull: false,
        primaryKey: true,
    },
    username: {
        type: Sequelize.STRING(50),
        allowNull: false,
        unique: true
    },
    password: {
        type: Sequelize.STRING(255),
        allowNull: false,
    },
    first_name: {
        type: Sequelize.STRING(50),
        allowNull: false,
    },
    last_name: {
        type: Sequelize.STRING(50),
        allowNull: false,
    },
    email: {
        type: Sequelize.STRING(150),
        allowNull: true,
    },
    phone_number: {
        type: Sequelize.STRING(15),
        allowNull: true,
    },
    created_at: {
        type: Sequelize.DATE,
        allowNull: true,
        defaultValue: Sequelize.NOW,
    },
}, {
    timestamps: false, // Disable automatic createdAt & updatedAt fields
});

module.exports = User;

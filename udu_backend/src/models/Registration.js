const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const Registration = new Schema({
    fullname: { type: String, required: true },
    phone: { type: String, required: true },
    email: { type: String, required: true },
    highschool: { type: String, required: true },
    major: { type: String, required: true },
    createdAt: { type: Date, default: Date.now },
});

module.exports = mongoose.model('Registration', Registration);

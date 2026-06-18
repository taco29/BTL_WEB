const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const Staff = new Schema({
    name: { type: String, required: true },
    degree: { type: String },
    position: { type: String },
    email: { type: String },
    avatar: { type: String },
    researchInterests: { type: [String], default: [] },
    department: { type: String },
    description: { type: String }
}, {
    timestamps: true
});

module.exports = mongoose.model('Staff', Staff);

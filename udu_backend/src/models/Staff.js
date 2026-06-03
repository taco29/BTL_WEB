const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const Staff = new Schema({
    name: { type: String, required: true },
    degree: { type: String }, // e.g., 'TS', 'ThS', 'PGS.TS'
    position: { type: String }, // e.g., 'Trưởng bộ môn', 'Giảng viên'
    email: { type: String },
    avatar: { type: String },
    researchInterests: { type: [String], default: [] },
    department: { type: String }, // e.g., 'Công nghệ phần mềm'
    description: { type: String }
}, {
    timestamps: true
});

module.exports = mongoose.model('Staff', Staff);

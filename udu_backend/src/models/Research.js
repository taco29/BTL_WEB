const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const Research = new Schema({
    name: { type: String, required: true },
    type: { type: String }, // 'project' (Đề tài) or 'group' (Nhóm)
    leader: { type: String },
    members: { type: [String], default: [] },
    year: { type: String },
    status: { type: String },
    level: { type: String }, // 'Cấp Cơ sở', 'Cấp Bộ' etc.
    description: { type: String },
    link: { type: String },
    address: { type: String },
    memberCount: { type: Number }
}, {
    timestamps: true
});

module.exports = mongoose.model('Research', Research);

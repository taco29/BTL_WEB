const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const Article = new Schema({
    title: { type: String, maxLength: 255 },
    slug: { type: String, maxLength: 255, unique: true },
    thumbnail: { type: String, maxLength: 255 },
    content: { type: String }, // HTML content or short description
    type: { type: String }, // 'news', 'event', 'student_activity'
    category: { type: String }, // 'cchoa', 'dnhoa', 'qthoa', 'ttin' (for news)
    eventDetails: {
        dateString: { type: String }, // e.g., "17/03/2025" or "17 TH3"
        timeString: { type: String }, // e.g., "17:00 - 21:00"
        location: { type: String }
    },
    publishedAt: { type: Date, default: Date.now }
}, {
    timestamps: true
});

module.exports = mongoose.model('Article', Article);

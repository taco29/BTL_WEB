const mongoose = require('mongoose');
const slug = require('mongoose-slug-updater');

mongoose.plugin(slug);

const Schema = mongoose.Schema;

const Course = new Schema({
    name: { type: String, maxLength: 255 },
    description: { type: String },
    image: { type: String, maxLength: 255 },
    slug: { type: String, slug: 'name', unique: true },

    code: { type: String },
    duration: { type: String },
    intake: { type: String },
    campus: { type: String },

    learningOutcomes: [
        {
            lo_id: { type: String },
            lo_desc: { type: String },
            pis: [
                {
                    pi_id: { type: String },
                    pi_desc: { type: String }
                }
            ]
        }
    ],

    curriculum: [
        {
            semester: { type: String },
            courses: [
                {
                    name: { type: String },
                    credits: { type: String },
                    type: { type: String }
                }
            ]
        }
    ],

    createdAt: { type: Date, default: Date.now },
    updatedAt: { type: Date, default: Date.now },
});

module.exports = mongoose.model('Course', Course);

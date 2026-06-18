const mongoose = require('mongoose');
const slug = require('mongoose-slug-updater');

mongoose.plugin(slug);

const Schema = mongoose.Schema;

const Course = new Schema({
    name: { type: String, maxLength: 255 },
    description: { type: String },
    image: { type: String, maxLength: 255 },
    slug: { type: String, slug: 'name', unique: true },

    // Tổng quan
    code: { type: String }, // Mã ngành
    duration: { type: String }, // Thời gian
    intake: { type: String }, // Kỳ nhập học
    campus: { type: String }, // Cơ sở

    // Chuẩn đầu ra 
    learningOutcomes: [
        {
            lo_id: { type: String }, // LO1
            lo_desc: { type: String },
            pis: [
                {
                    pi_id: { type: String }, // PI 1.1
                    pi_desc: { type: String }
                }
            ]
        }
    ],

    // Cấu trúc chương trình
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

const mongoose = require('mongoose');
const Schema = mongoose.Schema;

// Định nghĩa cái khuôn (Schema) cho một khóa học
const Course = new Schema({
    name: { type: String, maxLength: 255 },        
    description: { type: String }, 
    image: { type: String, maxLength: 255 },       
    slug: { type: String, maxLength: 255 },        
    
    // Tổng quan
    code: { type: String }, // Mã ngành
    duration: { type: String }, // Thời gian
    intake: { type: String }, // Kỳ nhập học
    campus: { type: String }, // Cơ sở

    // Chuẩn đầu ra (Mảng các LO)
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

    // Cấu trúc chương trình (Mảng các học kỳ)
    curriculum: [
        {
            semester: { type: String }, // Học kỳ 1
            courses: [
                {
                    name: { type: String }, // Tiếng Anh
                    credits: { type: String }, // 4 tín chỉ
                    type: { type: String } // bat-buoc-chung
                }
            ]
        }
    ],

    createdAt: { type: Date, default: Date.now },  
    updatedAt: { type: Date, default: Date.now },  
});

module.exports = mongoose.model('Course', Course);

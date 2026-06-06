const Course = require('../models/Course'); // Gọi Model vào

class CourseController {
    // [GET] /chuong-trinh-dao-tao/aiot
    async aiot(req, res) {
        try {
            // Hút dữ liệu từ MongoDB có slug là 'aiot'
            const course = await Course.findOne({ slug: 'aiot' });

            // Ép kiểu dữ liệu của Mongoose sang Object Javascript thường và ném ra View
            res.render('courses/aiot', {
                course: course ? course.toObject() : null
            });
        } catch (error) {
            res.status(400).json({ error: 'Lỗi Database!' });
        }
    }

    // [GET] /chuong-trinh-dao-tao/udu
    async udu(req, res) {
        try {
            const course = await Course.findOne({ slug: 'udu' });
            res.render('courses/udu', {
                course: course ? course.toObject() : null
            });
        } catch (error) {
            res.status(400).json({ error: 'Lỗi Database!' });
        }
    }
}

module.exports = new CourseController();

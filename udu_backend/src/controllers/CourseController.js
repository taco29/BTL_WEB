const Course = require('../models/Course');

class CourseController {
    async aiot(req, res) {
        try {
            const course = await Course.findOne({ slug: 'aiot' });
            res.render('courses/aiot', {
                course: course ? course.toObject() : null
            });
        } catch (error) {
            res.status(400).json({ error: 'Lỗi Database' });
        }
    }

    async udu(req, res) {
        try {
            const course = await Course.findOne({ slug: 'udu' });
            res.render('courses/udu', {
                course: course ? course.toObject() : null
            });
        } catch (error) {
            res.status(400).json({ error: 'Lỗi Database' });
        }
    }
}

module.exports = new CourseController();

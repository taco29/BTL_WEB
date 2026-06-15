const Article = require('../models/Article');
const Course = require('../models/Course');
const Registration = require('../models/Registration');

class SiteController {
    async index(req, res, next) {
        try {
            const news = await Article.find({ type: 'news' }).sort({ publishedAt: -1 }).limit(6).lean();
            const events = await Article.find({ type: 'event' }).sort({ publishedAt: -1 }).limit(3).lean();
            const courses = await Course.find({}).lean();

            res.render('home', { news, events, courses });
        } catch (error) {
            next(error);
        }
    }

    contact(req, res) {
        res.render('contact');
    }

    async event(req, res, next) {
        try {
            const PAGE_SIZE = 6;
            const page = parseInt(req.query.page) || 1;

            const totalItems = await Article.countDocuments({ type: 'event' });
            const totalPages = Math.ceil(totalItems / PAGE_SIZE);

            const events = await Article.find({ type: 'event' })
                .sort({ publishedAt: -1 })
                .skip((page - 1) * PAGE_SIZE)
                .limit(PAGE_SIZE)
                .lean();

            res.render('event', { events, currentPage: page, totalPages });
        } catch (error) {
            next(error);
        }
    }

    async register(req, res, next) {
        try {
            const { fullname, phone, email, highschool, major } = req.body;

            if (!fullname || !phone || !email || !highschool || !major) {
                return res.status(400).json({ success: false, message: 'Vui lòng điền đầy đủ thông tin!' });
            }

            const registration = new Registration({
                fullname,
                phone,
                email,
                highschool,
                major
            });

            await registration.save();

            return res.status(200).json({ success: true, message: 'Đăng ký thành công!' });
        } catch (error) {
            return res.status(500).json({ success: false, message: 'Đã có lỗi xảy ra, vui lòng thử lại!', error: error.message });
        }
    }
}

module.exports = new SiteController();
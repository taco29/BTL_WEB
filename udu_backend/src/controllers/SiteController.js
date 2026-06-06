const Article = require('../models/Article');
const Course = require('../models/Course');

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
            const events = await Article.find({ type: 'event' }).lean();
            res.render('event', { events });
        } catch (error) {
            next(error);
        }
    }
}

module.exports = new SiteController();
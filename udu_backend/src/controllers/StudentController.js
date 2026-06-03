const Article = require('../models/Article');

class StudentController {
    async lienChiDoan(req, res, next) {
        try {
            const clubNews = await Article.find({ type: 'club_news' }).lean();
            res.render('sinh-vien/lien-chi-doan-clb', { clubNews });
        } catch (error) {
            next(error);
        }
    }

    async hoatDong(req, res, next) {
        try {
            const activities = await Article.find({ type: 'student_activity' }).lean();
            res.render('sinh-vien/hoat-dong-sinh-vien', { activities });
        } catch (error) {
            next(error);
        }
    }
}

module.exports = new StudentController();

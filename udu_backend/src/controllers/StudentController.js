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
            const PAGE_SIZE = 12;
            const page = parseInt(req.query.page) || 1;
            
            const totalItems = await Article.countDocuments({ type: 'student_activity' });
            const totalPages = Math.ceil(totalItems / PAGE_SIZE);

            const activities = await Article.find({ type: 'student_activity' })
                .sort({ createdAt: -1 })
                .skip((page - 1) * PAGE_SIZE)
                .limit(PAGE_SIZE)
                .lean();

            console.log('Rendering hoat-dong-sinh-vien with activities length:', activities.length);

            res.render('sinh-vien/hoat-dong-sinh-vien', { 
                activities,
                currentPage: page,
                totalPages
            });
        } catch (error) {
            next(error);
        }
    }
}

module.exports = new StudentController();

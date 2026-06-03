const Article = require('../models/Article');

class NewsController {
    async chungChiHoa(req, res, next) {
        try {
            const PAGE_SIZE = 6;
            const page = parseInt(req.query.page) || 1;
            
            const totalItems = await Article.countDocuments({ type: 'news', category: 'cchoa' });
            const totalPages = Math.ceil(totalItems / PAGE_SIZE);

            const news = await Article.find({ type: 'news', category: 'cchoa' })
                .skip((page - 1) * PAGE_SIZE)
                .limit(PAGE_SIZE)
                .lean();
                
            res.render('tin-tuc/chung-chi-hoa', { 
                news,
                currentPage: page,
                totalPages
            });
        } catch (error) {
            next(error);
        }
    }

    async doanhNghiepHoa(req, res, next) {
        try {
            const PAGE_SIZE = 6;
            const page = parseInt(req.query.page) || 1;

            const totalItems = await Article.countDocuments({ type: 'news', category: 'dnhoa' });
            const totalPages = Math.ceil(totalItems / PAGE_SIZE);

            const news = await Article.find({ type: 'news', category: 'dnhoa' })
                .skip((page - 1) * PAGE_SIZE)
                .limit(PAGE_SIZE)
                .lean();

            res.render('tin-tuc/doanh-nghiep-hoa', { 
                news,
                currentPage: page,
                totalPages
            });
        } catch (error) {
            next(error);
        }
    }

    async quocTeHoa(req, res, next) {
        try {
            const PAGE_SIZE = 6;
            const page = parseInt(req.query.page) || 1;

            const totalItems = await Article.countDocuments({ type: 'news', category: 'qthoa' });
            const totalPages = Math.ceil(totalItems / PAGE_SIZE);

            const news = await Article.find({ type: 'news', category: 'qthoa' })
                .skip((page - 1) * PAGE_SIZE)
                .limit(PAGE_SIZE)
                .lean();

            res.render('tin-tuc/quoc-te-hoa', { 
                news,
                currentPage: page,
                totalPages
            });
        } catch (error) {
            next(error);
        }
    }

    async tinKhac(req, res, next) {
        try {
            const PAGE_SIZE = 6;
            const page = parseInt(req.query.page) || 1;

            const totalItems = await Article.countDocuments({ type: 'news', category: 'ttin' });
            const totalPages = Math.ceil(totalItems / PAGE_SIZE);

            const news = await Article.find({ type: 'news', category: 'ttin' })
                .skip((page - 1) * PAGE_SIZE)
                .limit(PAGE_SIZE)
                .lean();

            res.render('tin-tuc/tin-khac', { 
                news,
                currentPage: page,
                totalPages
            });
        } catch (error) {
            next(error);
        }
    }
}

module.exports = new NewsController();

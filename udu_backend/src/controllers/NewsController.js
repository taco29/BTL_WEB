const Article = require('../models/Article');

class NewsController {

    _getNewsData = async (req, category) => {
        const PAGE_SIZE = 12;
        const page = parseInt(req.query.page) || 1;
        const search = req.query.search || '';
        const sort = req.query.sort || '-createdAt';

        let queryObj = { type: 'news', category: category };
        if (search) {
            queryObj.title = { $regex: search, $options: 'i' };
        }

        let sortObj = {};
        const sortBy = sort.replace('-', '');
        const sortOrder = sort.startsWith('-') ? -1 : 1;
        sortObj[sortBy] = sortOrder;

        //TRUY VẤN VỚI DB
        const totalItems = await Article.countDocuments(queryObj);
        const totalPages = Math.ceil(totalItems / PAGE_SIZE);

        const news = await Article.find(queryObj)
            .sort(sortObj)
            .skip((page - 1) * PAGE_SIZE)
            .limit(PAGE_SIZE)
            .lean();

        return {
            news,
            currentPage: page,
            totalPages,
            searchQuery: search,
            currentSort: sort
        };
    }

    chungChiHoa = async (req, res, next) => {
        try {
            const data = await this._getNewsData(req, 'cchoa');
            res.render('tin-tuc/chung-chi-hoa', data);
        } catch (error) {
            next(error);
        }
    }

    doanhNghiepHoa = async (req, res, next) => {
        try {
            const data = await this._getNewsData(req, 'dnhoa');
            res.render('tin-tuc/doanh-nghiep-hoa', data);
        } catch (error) {
            next(error);
        }
    }

    quocTeHoa = async (req, res, next) => {
        try {
            const data = await this._getNewsData(req, 'qthoa');
            res.render('tin-tuc/quoc-te-hoa', data);
        } catch (error) {
            next(error);
        }
    }

    tinKhac = async (req, res, next) => {
        try {
            const data = await this._getNewsData(req, 'ttin');
            res.render('tin-tuc/tin-khac', data);
        } catch (error) {
            next(error);
        }
    }
}

module.exports = new NewsController();


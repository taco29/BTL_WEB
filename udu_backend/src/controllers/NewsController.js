const Article = require('../models/Article');

class NewsController {

    // Hàm dùng chung xử lý Tìm kiếm, Sắp xếp và Phân trang cho tất cả các trang tin tức
    _getNewsData = async (req, category) => {
        const PAGE_SIZE = 12;
        const page = parseInt(req.query.page) || 1;

        // Lấy từ khóa tìm kiếm và tiêu chí sắp xếp từ URL (Method GET)
        const search = req.query.search || '';
        const sort = req.query.sort || '-createdAt'; // Mặc định sắp xếp theo ngày tạo mới nhất (giảm dần)

        // 1. XÂY DỰNG QUERY TÌM KIẾM
        let queryObj = { type: 'news', category: category };
        if (search) {
            // Tìm kiếm gần đúng (regex) theo trường `title`, không phân biệt hoa thường ('i')
            queryObj.title = { $regex: search, $options: 'i' };
        }

        // 2. XÂY DỰNG OBJECT SẮP XẾP
        let sortObj = {};
        // VD: sort='title' -> tăng dần, sort='-title' -> giảm dần
        const sortBy = sort.replace('-', '');
        const sortOrder = sort.startsWith('-') ? -1 : 1;
        sortObj[sortBy] = sortOrder;

        // 3. THỰC THI TRUY VẤN VỚI DB
        const totalItems = await Article.countDocuments(queryObj);
        const totalPages = Math.ceil(totalItems / PAGE_SIZE);

        const news = await Article.find(queryObj)
            .sort(sortObj)
            .skip((page - 1) * PAGE_SIZE)
            .limit(PAGE_SIZE)
            .lean();

        // Trả về một object chứa toàn bộ dữ liệu cần thiết cho View
        return {
            news,
            currentPage: page,
            totalPages,
            searchQuery: search, // Trả lại từ khóa để nhét vào ô input trên giao diện
            currentSort: sort    // Trả lại tiêu chí để select box hiển thị đúng
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


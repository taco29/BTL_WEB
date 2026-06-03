const Staff = require('../models/Staff');

class IntroductionController {
    gioiThieuChung(req, res) {
        res.render('introduction/gioi-thieu-chung');
    }

    trietLy(req, res) {
        res.render('introduction/triet-ly-gd-dau-an-dao-tao');
    }

    lichSu(req, res) {
        res.render('introduction/lich-su-hinh-thanh-pt');
    }

    async giangVien(req, res, next) {
        try {
            const staffs = await Staff.find({}).lean();
            res.render('introduction/doi-ngu-giang-vien', { staffs });
        } catch (error) {
            next(error);
        }
    }

    coCau(req, res) {
        res.render('introduction/co-cau-to-chuc');
    }
}

module.exports = new IntroductionController();

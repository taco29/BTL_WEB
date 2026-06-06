const express = require('express');
const router = express.Router();

const introductionController = require('../controllers/IntroductionController');

router.get('/gioi-thieu-chung', introductionController.gioiThieuChung);
router.get('/triet-ly-gd-dau-an-dao-tao', introductionController.trietLy);
router.get('/lich-su-hinh-thanh-pt', introductionController.lichSu);
router.get('/doi-ngu-giang-vien', introductionController.giangVien);
router.get('/co-cau-to-chuc', introductionController.coCau);

module.exports = router;

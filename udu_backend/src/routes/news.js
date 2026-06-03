const express = require('express');
const router = express.Router();

const newsController = require('../controllers/NewsController');
router.get('/chung-chi-hoa', newsController.chungChiHoa);
router.get('/doanh-nghiep-hoa', newsController.doanhNghiepHoa);
router.get('/quoc-te-hoa', newsController.quocTeHoa);
router.get('/tin-khac', newsController.tinKhac);

module.exports = router;
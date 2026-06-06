const express = require('express');
const router = express.Router();

const researchController = require('../controllers/ResearchController');

router.get('/nhom-nghien-cuu', researchController.nhomNghienCuu);
router.get('/de-tai-nckh', researchController.deTai);

module.exports = router;

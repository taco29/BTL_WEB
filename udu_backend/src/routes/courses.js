const express = require('express');
const router = express.Router();

const courseController = require('../controllers/CourseController');

router.get('/aiot', courseController.aiot);
router.get('/udu', courseController.udu);

module.exports = router;

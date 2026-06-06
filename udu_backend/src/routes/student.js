const express = require('express');
const router = express.Router();

const studentController = require('../controllers/StudentController');

router.get('/lien-chi-doan-clb', studentController.lienChiDoan);
router.get('/hoat-dong-sinh-vien', studentController.hoatDong);

module.exports = router;

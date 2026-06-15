const express = require('express');
const router = express.Router();

const siteController = require('../controllers/SiteController');
router.get('/lien-he', siteController.contact);
router.get('/su-kien', siteController.event);
router.post('/register', siteController.register);
router.get('/', siteController.index);

module.exports = router;
const Research = require('../models/Research');

class ResearchController {
    async nhomNghienCuu(req, res, next) {
        try {
            const groups = await Research.find({ type: 'group' }).lean();
            res.render('research/nhom-nghien-cuu', { groups });
        } catch (error) {
            next(error);
        }
    }

    async deTai(req, res, next) {
        try {
            const projects = await Research.find({ type: 'project' }).lean();
            res.render('research/de-tai-nckh', { projects });
        } catch (error) {
            next(error);
        }
    }
}

module.exports = new ResearchController();

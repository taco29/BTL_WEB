const siteRouter = require('./site');
const coursesRouter = require('./courses');
const introductionRouter = require('./introduction');
const newsRouter = require('./news');
const researchRouter = require('./research');
const studentRouter = require('./student');

function route(app) {
    app.use('/chuong-trinh-dao-tao', coursesRouter);
    app.use('/gioi-thieu', introductionRouter);
    app.use('/tin-tuc', newsRouter);
    app.use('/nghien-cuu', researchRouter);
    app.use('/sinh-vien', studentRouter);

    app.use('/', siteRouter);
}

module.exports = route;
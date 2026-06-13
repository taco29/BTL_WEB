const siteRouter = require('./site');
const coursesRouter = require('./courses');
const introductionRouter = require('./introduction');
const newsRouter = require('./news');
const researchRouter = require('./research');
const studentRouter = require('./student');
const { spawn } = require('child_process');
const path = require('path');

function route(app) {
    app.use('/chuong-trinh-dao-tao', coursesRouter);
    app.use('/gioi-thieu', introductionRouter);
    app.use('/tin-tuc', newsRouter);
    app.use('/nghien-cuu', researchRouter);
    app.use('/sinh-vien', studentRouter);

    app.use('/', siteRouter);

    app.post('/api/chat', (req, res) => {
        const question = req.body.question;
        
        if (!question) {
            return res.status(400).json({ answer: "Vui lòng nhập câu hỏi!" });
        }

        const pythonScriptPath = path.join(__dirname, '../../../chatbot/main.py');
        const pythonProcess = spawn('python', [pythonScriptPath, question], {
            cwd: path.join(__dirname, '../../../chatbot'),
            env: { ...process.env, PYTHONIOENCODING: 'utf-8' }
        });

        let botAnswer = '';
        let errorOutput = '';

        const timeout = setTimeout(() => {
            pythonProcess.kill();
            if (!res.headersSent) {
                res.status(500).json({ answer: "Chatbot mất quá nhiều thời gian, vui lòng thử lại!" });
            }
        }, 180000);

        pythonProcess.stdout.on('data', (data) => {
            botAnswer += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
            errorOutput += data.toString();
            console.error(`[Chatbot Python Error]: ${data}`);
        });

        pythonProcess.on('close', (code) => {
            clearTimeout(timeout);
            if (res.headersSent) return;
            if (code !== 0 && code !== null) {
                console.error(`[Chatbot] Python exited with code ${code}. Stderr: ${errorOutput}`);
                return res.status(500).json({ answer: "Hệ thống đang bận, vui lòng thử lại sau!" });
            }
            res.json({ answer: botAnswer.trim() });
        });
    });
}

module.exports = route;
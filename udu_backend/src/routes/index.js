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

    const chatbotDir = path.join(__dirname, '../../../chatbot');
    const pythonProcess = spawn('python', ['-u', 'main.py'], {
        cwd: chatbotDir,
        env: { ...process.env, PYTHONIOENCODING: 'utf-8' }
    });

    let currentResolver = null;

    pythonProcess.stdout.on('data', (data) => {
        const output = data.toString().trim();
        
        if (output.includes("READY")) {
            console.log("da cho embmodel vao ram!");
            return;
        }

        if (currentResolver) {
            try {
                const lines = output.split('\n').filter(l => l.trim());
                const lastLine = lines[lines.length - 1];
                const parsed = JSON.parse(lastLine);
                currentResolver(parsed);
            } catch (error) {
                currentResolver({ answer: output });
            }
            currentResolver = null;
        }
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error("[🔥 Python Log]:", data.toString());
    });

    app.post('/api/chat', (req, res) => {
        const question = req.body.question;
        
        if (!question) {
            return res.status(400).json({ answer: "Vui lòng nhập câu hỏi!" });
        }

        if (currentResolver) {
            return res.status(503).json({ answer: "Hệ thống đang bận xử lý, vui lòng chờ trong giây lát..." });
        }

        currentResolver = (result) => {
            if (result.error) {
                return res.status(500).json({ answer: "Lỗi xử lý AI: " + result.error });
            }
            res.json({ answer: result.answer });
        };

        pythonProcess.stdin.write(question + '\n');
    });
}
module.exports = route;
const mongoose = require('mongoose');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

async function importAll() {
    try {
        await mongoose.connect(process.env.MONGODB_URI || 'mongodb://127.0.0.1:27017/udu_database');
        console.log('Connected to MongoDB...');

        const backupDir = path.join(__dirname, 'db_backup');
        if (!fs.existsSync(backupDir)) {
            console.log('Không tìm thấy thư mục db_backup! Vui lòng copy thư mục này từ máy của bạn bè vào dự án.');
            process.exit(1);
        }

        const files = fs.readdirSync(backupDir).filter(f => f.endsWith('.json'));

        for (let file of files) {
            const collectionName = file.replace('.json', '');
            const filePath = path.join(backupDir, file);
            
            // Đọc dữ liệu từ file
            const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
            if (data.length === 0) continue;

            console.log(`Đang nạp ${data.length} bản ghi vào bảng '${collectionName}'...`);
            
            const collection = mongoose.connection.db.collection(collectionName);
            
            // Tuỳ chọn: Xoá sạch dữ liệu cũ trong bảng trước khi import (để giống hệt máy gốc)
            // await collection.deleteMany({});
            
            for (let item of data) {
                // Sửa _id string thành ObjectId nếu có
                if (item._id && typeof item._id === 'string') {
                    item._id = new mongoose.Types.ObjectId(item._id);
                }
                
                // Import từng dòng bằng replaceOne với upsert
                await collection.replaceOne(
                    { _id: item._id },
                    item,
                    { upsert: true }
                );
            }
        }

        console.log('\n✅ Import toàn bộ dữ liệu thành công!');
        process.exit(0);
    } catch (error) {
        console.error('Lỗi khi import:', error);
        process.exit(1);
    }
}

importAll();

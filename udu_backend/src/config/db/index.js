const mongoose = require('mongoose');

async function connect() {
    try {
        await mongoose.connect('mongodb://127.0.0.1:27017/udu_database');
        console.log('Ket noi mongodb thanh cong')
    } catch (error) {
        console.log('Ket noi mongodb that bai')
    }

}

module.exports = { connect };
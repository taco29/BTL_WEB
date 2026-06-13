const express = require('express');
const { engine } = require('express-handlebars');
const db = require('./config/db');

const app = express();
const port = 3000;
const path = require('path');
const route = require('./routes');

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

route(app);
db.connect();

app.use('/udu_clone', express.static(path.join(__dirname, 'public')));

const handlebarsHelpers = require('./utils/handlebarsHelpers');

app.engine('hbs', engine({ 
    extname: 'hbs',
    helpers: handlebarsHelpers
}));
app.set('view engine', 'hbs');
app.set('views', path.join(__dirname, 'resources/views'));




app.listen(port, () => {
    console.log(`App running on http://localhost:${port}`);
});

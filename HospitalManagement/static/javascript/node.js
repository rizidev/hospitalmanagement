const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('mysql');

const app = express();
const port = 3000;

app.use(bodyParser.json());
app.use(express.static('public'));

const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'password',
    database: 'hospital'
});

db.connect((err) => {
    if (err) throw err;
    console.log('Database connected!');
});

// Add patient
app.post('/add-patient', (req, res) => {
    const { name, age, disease } = req.body;
    const query = 'INSERT INTO patients (name, age, disease) VALUES (?, ?, ?)';
    db.query(query, [name, age, disease], (err, result) => {
        if (err) throw err;
        res.send('Patient added!');
    });
});

// Get patients
app.get('/patients', (req, res) => {
    db.query('SELECT * FROM patients', (err, results) => {
        if (err) throw err;
        res.json(results);
    });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});

// backend/routes auth.js

import { Router } from 'express';
import { pool } from '../db.js';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';


const router = Router();
const SECRET = 'your_secret_key';


// Регистрация
router.post('/register', async (req, res) => {
const { email, password, role } = req.body;
const hash = await bcrypt.hash(password, 10);


try {
const result = await pool.query(
'INSERT INTO users(email, password, role) VALUES($1,$2,$3) RETURNING id, email, role',
[email, hash, role]
);
res.json(result.rows[0]);
} catch (err) {
res.status(400).json({ error: err.message });
}
});


// Логин
router.post('/login', async (req, res) => {
const { email, password } = req.body;
try {
const result = await pool.query('SELECT * FROM users WHERE email = $1', [email]);
const user = result.rows[0];
if (!user) return res.status(400).json({ error: 'User not found' });


const match = await bcrypt.compare(password, user.password);
if (!match) return res.status(400).json({ error: 'Wrong password' });


const token = jwt.sign({ id: user.id, role: user.role }, SECRET, { expiresIn: '2h' });
res.json({ token, role: user.role });
} catch (err) {
res.status(500).json({ error: err.message });
}
});


export default router;
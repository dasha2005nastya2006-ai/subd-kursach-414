// backend/routes tests.js

import { Router } from 'express';
import { pool } from '../db.js';


const router = Router();


// Все тесты
router.get('/', async (req, res) => {
const { rows } = await pool.query(
'SELECT id, title, duration_minutes FROM tests WHERE is_published = true'
);
res.json(rows);
});


// Один тест с вопросами
router.get('/:id', async (req, res) => {
const testId = req.params.id;


const test = await pool.query(
'SELECT id, title FROM tests WHERE id = $1',
[testId]
);


const questions = await pool.query(`
SELECT q.id, q.text,
json_agg(json_build_object('id', a.id, 'text', a.text)) AS answers
FROM questions q
JOIN answers a ON a.question_id = q.id
WHERE q.test_id = $1
GROUP BY q.id
`, [testId]);


res.json({
...test.rows[0],
questions: questions.rows
});
});


export default router;
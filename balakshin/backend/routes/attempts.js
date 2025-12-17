// backend/routes attempts.js

import { Router } from 'express';
import { pool } from '../db.js';


const router = Router();


router.post('/', async (req, res) => {
const { testId, studentId, answers } = req.body;


const attempt = await pool.query(
'INSERT INTO test_attempts(test_id, student_id) VALUES($1,$2) RETURNING id',
[testId, studentId]
);


const attemptId = attempt.rows[0].id;


for (const [questionId, answerId] of Object.entries(answers)) {
await pool.query(
'INSERT INTO student_answers(attempt_id, question_id, answer_id) VALUES($1,$2,$3)',
[attemptId, questionId, answerId]
);
}


res.json({ success: true, attemptId });
});


export default router;
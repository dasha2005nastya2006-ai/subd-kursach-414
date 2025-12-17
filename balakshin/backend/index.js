// backend index.js

import express from 'express';
import cors from 'cors';


import testsRoutes from './routes/tests.js';
import attemptsRoutes from './routes/attempts.js';


const app = express();
app.use(cors());
app.use(express.json());


app.use('/api/tests', testsRoutes);
app.use('/api/attempts', attemptsRoutes);


app.listen(3001, () => {
console.log('Backend started on http://localhost:3001');
});
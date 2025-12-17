// backend db.js

import pkg from 'pg';
const { Pool } = pkg;


export const pool = new Pool({
user: 'postgres',
password: 'password',
host: 'localhost',
port: 5432,
database: 'testing_system'
});
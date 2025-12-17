// frontend router.ts

import { renderLogin } from './pages/login.js';
import { renderDashboard } from './pages/dashboard.js';
import { renderTests } from './pages/tests.js';
import { renderPassTest } from './pages/passTest.js';
import { renderResults } from './pages/results.js';


export function router() {
const path = location.hash.slice(1) || '/login';


if (path === '/login') renderLogin();
else if (path === '/dashboard') renderDashboard();
else if (path === '/tests') renderTests();
else if (path.startsWith('/tests/')) renderPassTest(+path.split('/')[2]);
else if (path === '/results') renderResults();
}
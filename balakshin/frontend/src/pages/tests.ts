// frontend/pages tests.ts

import { api } from '../api.js';
import { layout } from '../components/layout.js';


export async function renderTests() {
const tests = await api.getTests();
const html = tests.map(t => `
<div class="card">
<h3>${t.title}</h3>
<p>Время: ${t.duration} мин</p>
<a href="#/tests/${t.id}">Начать</a>
</div>
`).join('');


document.getElementById('app')!.innerHTML = layout(html);
}
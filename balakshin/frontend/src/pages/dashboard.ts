import { api } from '../api.js';
import { layout } from '../components/layout.js';

export async function renderDashboard() {
  const app = document.getElementById('app')!;
  const tests = await api.getTests();
  app.innerHTML = layout(`
    <h2>Список тестов</h2>
    <ul>
      ${tests.map(t => `<li><a href="#/passTest/${t.id}">${t.title}</a></li>`).join('')}
    </ul>
  `);
}

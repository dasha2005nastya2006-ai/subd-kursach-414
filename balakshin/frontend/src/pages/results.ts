// frontend/pages results.ts

import { layout } from '../components/layout.js';
import { state } from '../state.js';

export function renderResults() {
  const answersHtml = Object.entries(state.answers)
    .map(([q, a]) => `<li>Вопрос ${q}: ответ ${a}</li>`)
    .join('');

  document.getElementById('app')!.innerHTML = layout(`
    <h2>Результаты</h2>
    <ul>${answersHtml}</ul>
  `);
}

// frontend/pages passTest.ts

import { api } from '../api.js';
import { layout } from '../components/layout.js';
import { questionBlock } from '../components/question.js';
import { state } from '../state.js';

export async function renderPassTest(id: number) {
  const test = await api.getTest(id);

  document.getElementById('app')!.innerHTML = layout(`
    <h2>${test.title}</h2>
    ${test.questions.map(questionBlock).join('')}
    <button class="btn-primary" id="finishBtn">Завершить</button>
  `);

  document.getElementById('finishBtn')!.onclick = () => {
    console.log('Ответы студента:', state.answers);

    // 👉 тут позже будет отправка на backend
    location.hash = '/results';
  };
}


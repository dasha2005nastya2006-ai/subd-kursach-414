// frontend main.ts

import { router } from './router.js';
import { state } from './state.js';

window.addEventListener('hashchange', router);
window.addEventListener('load', router);

(window as any).saveAnswer = (questionId: number, answerId: number) => {
  state.answers[questionId] = answerId;
};

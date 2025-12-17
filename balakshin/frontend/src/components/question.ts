// frontend/components question.ts

import { state } from '../state.js';

export function questionBlock(question: {
  id: number;
  text: string;
  answers: { id: number; text: string }[];
}) {
  return `
    <div class="card">
      <strong>${question.text}</strong>
      ${question.answers
        .map(
          a => `
            <div>
              <label>
                <input 
                  type="radio" 
                  name="q${question.id}" 
                  value="${a.id}"
                  onchange="window.saveAnswer(${question.id}, ${a.id})"
                />
                ${a.text}
              </label>
            </div>
          `
        )
        .join('')}
    </div>
  `;
}


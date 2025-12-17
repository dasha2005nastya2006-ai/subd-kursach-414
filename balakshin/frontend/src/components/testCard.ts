// frontend/components testCard.ts 

export function testCard(test: { id: number; title: string; duration: number }) {
  return `
    <div class="card">
      <h3>${test.title}</h3>
      <p>Время: ${test.duration} мин</p>
      <a href="#/tests/${test.id}">Начать</a>
    </div>
  `;
}

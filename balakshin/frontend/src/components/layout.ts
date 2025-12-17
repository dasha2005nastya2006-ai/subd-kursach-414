// frontend/components layout.ts

export function layout(content: string) {
return `
<div class="layout">
<div class="sidebar">
<h2>Test System</h2>
<a href="#/dashboard">Главная</a>
<a href="#/tests">Тесты</a>
<a href="#/results">Результаты</a>
</div>
<div class="content">${content}</div>
</div>
`;
}
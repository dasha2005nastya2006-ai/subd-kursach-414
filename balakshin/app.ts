import type { Test, Question } from "./types";
import { login, getTests, getQuestions } from "./api";

const root = document.getElementById("root") as HTMLDivElement;

let currentPage: "login" | "tests" | "test" = "login";
let currentTestQuestions: Question[] = [];
let currentAnswers: number[] = [];

function renderLogin() {
    root.innerHTML = `
        <h2>Вход в систему</h2>
        <input id="email" placeholder="Email" />
        <input id="password" type="password" placeholder="Пароль" />
        <button id="loginBtn">Войти</button>
    `;
    const loginBtn = document.getElementById("loginBtn")!;
    loginBtn.addEventListener("click", async () => {
        const email = (document.getElementById("email") as HTMLInputElement).value;
        const password = (document.getElementById("password") as HTMLInputElement).value;
        const success = await login(email, password);
        if (success) {
            currentPage = "tests";
            renderTests();
        } else {
            alert("Ошибка входа");
        }
    });
}

function renderTests() {
    getTests().then(tests => {
        root.innerHTML = "<h2>Доступные тесты</h2>";
        const list = document.createElement("ul");
        tests.forEach(test => {
            const li = document.createElement("li");
            li.textContent = test.name;
            li.style.cursor = "pointer";
            li.addEventListener("click", () => {
                currentPage = "test";
                startTest();
            });
            list.appendChild(li);
        });
        root.appendChild(list);
    });
}

function startTest() {
    getQuestions().then(questions => {
        currentTestQuestions = questions;
        currentAnswers = new Array(questions.length).fill(-1);
        renderTest();
    });
}

function renderTest() {
    root.innerHTML = "<h2>Прохождение теста</h2>";
    currentTestQuestions.forEach((q, i) => {
        const div = document.createElement("div");
        div.innerHTML = `<p>${q.text}</p>`;
        q.answers.forEach((a, idx) => {
            const label = document.createElement("label");
            const radio = document.createElement("input");
            radio.type = "radio";
            radio.name = `q${i}`;
            radio.value = String(idx);
            radio.addEventListener("change", () => currentAnswers[i] = idx);
            label.appendChild(radio);
            label.appendChild(document.createTextNode(a));
            div.appendChild(label);
            div.appendChild(document.createElement("br"));
        });
        root.appendChild(div);
    });
    const btn = document.createElement("button");
    btn.textContent = "Завершить тест";
    btn.addEventListener("click", finishTest);
    root.appendChild(btn);
}

function finishTest() {
    let score = 0;
    currentTestQuestions.forEach((q, i) => {
        if (currentAnswers[i] === q.correct) score++;
    });
    alert(`Результат: ${score} из ${currentTestQuestions.length}`);
}

// Инициализация
renderLogin();

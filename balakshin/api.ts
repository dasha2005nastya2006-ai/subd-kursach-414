import type { Test, Question } from "./types";

export const login = async (email: string, password: string): Promise<boolean> => {
    return email.length > 0 && password.length > 0;
};

export const getTests = async (): Promise<Test[]> => {
    return [
        { id: 1, name: "Основы баз данных" },
        { id: 2, name: "SQL" }
    ];
};

export const getQuestions = async (): Promise<Question[]> => {
    return [
        {
            id: 1,
            text: "Что такое первичный ключ?",
            answers: ["Уникальный идентификатор записи", "Тип данных", "Внешний ключ"],
            correct: 0
        },
        {
            id: 2,
            text: "SQL используется для:",
            answers: ["Создания графики", "Работы с базами данных", "Разработки игр"],
            correct: 1
        }
    ];
};

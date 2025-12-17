export interface Test {
    id: number;
    name: string;
}

export interface Question {
    id: number;
    text: string;
    answers: string[];
    correct: number;
}

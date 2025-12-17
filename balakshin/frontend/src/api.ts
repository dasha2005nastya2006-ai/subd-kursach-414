// frontend api.ts

export const api = {
login: async (email: string, password: string) => {
return { token: 'mock-token', role: 'student' };
},


getTests: async () => [
{ id: 1, title: 'Математика', duration: 30 },
{ id: 2, title: 'Информатика', duration: 25 }
],


getTest: async (id: number) => ({
id,
title: 'Математика',
questions: [
{
id: 1,
text: '2 + 2 = ?',
answers: [
{ id: 1, text: '3' },
{ id: 2, text: '4' }
]
}
]
})
};
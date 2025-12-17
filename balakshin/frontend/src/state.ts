//frontend state.ts

export const state = {
  token: null as string | null,
  userRole: 'student',
  answers: {} as Record<number, number> // questionId -> answerId
};
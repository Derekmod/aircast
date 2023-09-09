export interface Question {
    question: string
    correct_answer: string
    other_answers: string[];
    shuffled_answers?: string[];
    isAnswered?: boolean;
    isCorrect?: boolean;
}

const shuffle = ([...arr]) => {
    let m = arr.length;
    while (m) {
        const i = Math.floor(Math.random() * m--);
        [arr[m], arr[i]] = [arr[i], arr[m]];
    }
    return arr;
};

export function getAllAnswers(question: Question): string[] {
    return shuffle([question.correct_answer, ...question.other_answers]);
}
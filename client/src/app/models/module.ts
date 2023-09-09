import { Question } from './question';

export interface Module {
    name: string;
    blurb: string;
    questions: Question[];
}
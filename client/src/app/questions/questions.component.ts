import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Question } from '../models';

@Component({
  selector: 'app-questions',
  templateUrl: './questions.component.html',
  styleUrls: ['./questions.component.scss']
})
export class QuestionsComponent {
  @Input() questions: Question[] = [];
  @Input() totalQuestions: number = 0;

  @Output() continue: EventEmitter<any> = new EventEmitter<any>();
  @Output() completeLesson: EventEmitter<any> = new EventEmitter<any>();

  selectAnswer(question: Question, answer: string) {
    question.isCorrect = question.correct_answer === answer;
    question.isAnswered = true;
  }

  clickContinue() {
    this.continue.emit();
  }

  clickComplete() {
    this.completeLesson.emit();
  }

}

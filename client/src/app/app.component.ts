import { Component, OnInit } from '@angular/core';
import { ContentService } from './content.service';

import { Question, getAllAnswers } from './models';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  questions: Question[] = [];
  title: string = '';
  content: string = '';
  totalQuestions: number = 0;
  loadedQuestions: number = 0;
  progress: number = 0;

  inQuestions: boolean = false;
  getAllAnswers = getAllAnswers;

  // Infinite scroll settings
  scrollDistance = 1.5;
  scrollUpDistance = 1.5;
  throttle = 300;

  constructor(private contentService: ContentService) {}

  ngOnInit() {
    this.totalQuestions = this.contentService.getTotalContentCount();
    this.content = this.contentService.getContent();
    this.title = this.contentService.getTitle();
  }

  loadMoreItems() {
    this.contentService.getQuestions(this.loadedQuestions, 1).subscribe(newQuestions => {
      this.questions = [...this.questions, ...newQuestions];
      this.loadedQuestions += newQuestions.length;
      this.updateProgress();
    });
  }

  updateProgress() {
    this.progress = (this.loadedQuestions / this.totalQuestions) * 100;
  }

  onScroll() {
    // this.loadMoreItems();
  }

  continue() {
    this.loadMoreItems();
    this.inQuestions = true;
  }

  selectAnswer(question: Question, answer: string) {
    question.isCorrect = question.correct_answer === answer;
    question.isAnswered = true;
  }

  goBack() {
    // Use Angular's Router to navigate to the previous or specific route
    // this.router.navigate(['/previous-route']);
  }

}

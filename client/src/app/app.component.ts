import { Component, OnInit } from '@angular/core';
import { ContentService } from './content.service';
import { of } from 'rxjs';

import { Question } from './models';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  state: 'overview' | 'message' | 'questions' | 'results' = 'overview';

  questions: Question[] = [];
  title: string = '';
  content: string = '';
  totalQuestions: number = 0;
  loadedQuestions: number = 0;
  progress: number = 0;

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
  }

  moveToNextScreen() {
    this.state = 'message';
    of(null).pipe(
      delay(1500)
    ).subscribe(() => {
      this.currentScreen = 'nextComponent';
    });
  }

  goBack() {
    // Use Angular's Router to navigate to the previous or specific route
    // this.router.navigate(['/previous-route']);
  }

}

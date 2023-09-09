import { Injectable } from '@angular/core';
import { Observable, of, Subject } from 'rxjs';
import { HttpClient } from '@angular/common/http';

import { PaperCurriculum, Question, getAllAnswers } from './models';

@Injectable({
  providedIn: 'root'
})
export class ContentService {
  private url: string = `http://127.0.0.1:5000/curriculum`;
  private testUrl = 'https://arxiv.org/pdf/1706.03762.pdf';
  private storage: Storage;

  constructor(private http: HttpClient) {
    this.storage = localStorage;
  }

  async getPaper(): Promise<any> {
    const currPaper = await this.http.post<PaperCurriculum>(
      this.url, { data: this.testUrl }
    ).toPromise();
    this.storage.setItem('paper', JSON.stringify(currPaper));
    return currPaper;
  }

  getTitle(): string {
    return '';
    // return this.paperCurriculum.overview_module.name;
  }

  getContent(): string {
    return '';
    // return this.paperCurriculum.overview_module.blurb;
  }

  getQuestions(start: number, count: number): Observable<Question[]> {
    // const currQuestions = [].slice(start, start + count);
    // for (const question of currQuestions) {
    //   question.shuffled_answers = getAllAnswers(question);
    // }
    return of([]);
  }

  getTotalContentCount(): number {
    return 0;
    // return this.paperCurriculum.overview_module.questions.length;
  }
}

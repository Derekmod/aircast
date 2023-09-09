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
    return 'Attention is All You Need';
    // const paper = this.storage.getItem('paper');
    // return paper && JSON.parse(paper) && JSON.parse(paper).overview_module.name;
  }

  getContent(): string {
    const paper = this.storage.getItem('paper');
    return paper && JSON.parse(paper) && JSON.parse(paper).overview_module.blurb;
  }

  getQuestions(start: number, count: number): Observable<Question[]> {
    const paper = this.storage.getItem('paper');
    const currQuestions = paper && JSON.parse(paper) && JSON.parse(paper).overview_module.questions.slice(start, start + count);
    for (const question of currQuestions) {
      question.shuffled_answers = getAllAnswers(question);
    }
    return of(currQuestions);
  }

  getTotalContentCount(): number {
    const paper = this.storage.getItem('paper');
    return paper && JSON.parse(paper) && JSON.parse(paper).overview_module.questions.length;
  }
}

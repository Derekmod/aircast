import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

import { Summary } from './models';

@Injectable({
  providedIn: 'root'
})
export class ContentService {
  private summary: Summary = {
    title: 'Attention is All You Need',
    content: [
      'Item 1', 'Item 2', 'Item 3',
    ],
  };

  getTitle(): string {
    return this.summary.title;
  }

  getContent(start: number, count: number): Observable<string[]> {
    return of(this.summary.content.slice(start, start + count));
  }

  getTotalContentCount(): number {
    return this.summary.content.length;
  }
}

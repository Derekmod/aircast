import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ContentService {
  private content = [
    // Your content here. For example:
    'Item 1', 'Item 2', 'Item 3', // ...
  ];

  getContent(start: number, count: number): Observable<string[]> {
    return of(this.content.slice(start, start + count));
  }

  getTotalContentCount(): number {
    return this.content.length;
  }
}

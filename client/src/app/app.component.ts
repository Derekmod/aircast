import { Component, OnInit } from '@angular/core';
import { ContentService } from './content.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  items: string[] = [];
  totalItems: number = 0;
  loadedItems: number = 0;
  progress: number = 0;

  // Infinite scroll settings
  scrollDistance = 1.5;
  scrollUpDistance = 1.5;
  throttle = 300;

  constructor(private contentService: ContentService) {}

  ngOnInit() {
    this.totalItems = this.contentService.getTotalContentCount();
    this.loadMoreItems();
  }

  loadMoreItems() {
    this.contentService.getContent(this.loadedItems, 10).subscribe(newItems => {
      this.items = [...this.items, ...newItems];
      this.loadedItems += newItems.length;
      this.updateProgress();
    });
  }

  updateProgress() {
    this.progress = (this.loadedItems / this.totalItems) * 100;
  }

  onScroll() {
    this.loadMoreItems();
  }

  continue() {
    // Implement your logic to move forward with content from the service
  }
}

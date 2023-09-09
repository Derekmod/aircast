import { Component, OnInit } from '@angular/core';
import { ContentService } from './content.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  items: string[] = [];
  title: string = '';
  content: string = '';
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
    this.content = this.contentService.getContent();
    this.loadMoreItems();
    this.title = this.contentService.getTitle();
  }

  loadMoreItems() {
    // this.contentService.getContent(this.loadedItems, 1).subscribe(newItems => {
    //   this.items = [...this.items, ...newItems];
    //   this.loadedItems += newItems.length;
    //   this.updateProgress();
    // });
  }

  updateProgress() {
    this.progress = (this.loadedItems / this.totalItems) * 100;
  }

  onScroll() {
    this.loadMoreItems();
  }

  continue() {
    this.loadMoreItems();
  }

  goBack() {
    // Use Angular's Router to navigate to the previous or specific route
    // this.router.navigate(['/previous-route']);
  }

}

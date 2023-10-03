import { Component, ElementRef, ViewChild } from '@angular/core';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent {
  @ViewChild('searchText') public filterResult!: ElementRef;
  searchables: string[] = ["Patrick", "John", "Rose", "Thomas", "Jerry", "Chris", "Andrew"];

  present!: boolean;
  filterSearch!: string;


  // Upon input in searchtext input should add content unsafely to DOM
  public updateFilterText() {
    if (this.filterSearch in this.searchables) {
      this.present = true;
    }
    else {
      this.present = false;
    }
    const domElement = this.filterResult.nativeElement;
    const fragment = document.createRange().createContextualFragment(this.filterSearch);
    domElement.appendChild(fragment);
  }
}

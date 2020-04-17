import {Component} from '@angular/core';
import {DomSanitizer} from '@angular/platform-browser';


import {v4 as uuidv4} from 'uuid';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  imageWidth = 492;
  imageHeight = 128;
  noImageText = 'Изображение не загружено!';

  imageURL = undefined;
  requestId = undefined;
  vehicleType = undefined;
  licensePlateStd = undefined;
  licensePlateChars = undefined;

  constructor(private sanitizer: DomSanitizer) {
    this.clearOutput(true);
  }

  onFileNameChange(event: any) {
    this.clearOutput(true);
    this.requestId = uuidv4();

    const fileReader = new FileReader();
    fileReader.readAsArrayBuffer(event.target.files[0]);

    fileReader.onload = () => {
      const data = fileReader.result as ArrayBufferLike;
      const data64 = btoa(String.fromCharCode(...new Uint8Array(data)));

      console.log('IMAGE BASE64:', data64);
      this.imageURL = this.sanitizer.bypassSecurityTrustUrl('data:image/jpg;base64, ' + data64);

      const socket = new WebSocket('ws://' + location.hostname + '/ws');
      socket.onopen = () => {
        socket.send(data); console.log('SEND OK!');
      };
      socket.onmessage = (evt) => {
        if (evt.data === 'unknown') {
          this.clearOutput(false);
          alert('Неизвестный тип ГРЗ!');
        } else {
          const r = evt.data.split('.');
          this.vehicleType = r[0];
          this.licensePlateStd = r[1];
          this.licensePlateChars = r[2];
        }
        socket.close();
      };
      socket.onerror = (err) => {
        console.log('BAD SOCKET: ', err);
      };
    };
  }

  clearOutput(clearImage: boolean) {
    this.requestId = '-';
    this.vehicleType = '-';
    this.licensePlateStd = '-';
    this.licensePlateChars = '-';

    if (clearImage) {
      this.imageURL = `https://via.placeholder.com/${this.imageWidth}x${this.imageHeight}.png?text=${this.noImageText}`;
    }
  }
}

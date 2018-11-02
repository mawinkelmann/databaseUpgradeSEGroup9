# Greek Life Member Management System

- Install Python 3 and set up development environment: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/development_environment
- Follow the steps provided in the link.
- When you get to the installation of virtualenvwrapper you may need to use -H in the sudo to get it to install properly (e.g. sudo '''js-H''' pip3 install virtualenvwrapper)
- Stop after Python is installed.
- Install Crispy-Forms: https://bit.ly/2OicHU0
- In a terminal navigate to the main GLMMS folder (you will know that this is the correct one because it will contain a file named manage.py)
- Ensure that your virtual environment is still active and enter the command: python3 manage.py runserver
- Open a browser window and navigate to: http://127.0.0.1:8000/




```js
  import { Component } from '@angular/core';
  import { MovieService } from './services/movie.service';

  @Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css'],
    providers: [ MovieService ]
  })
  export class AppComponent {
    title = 'app works!';
  }
```

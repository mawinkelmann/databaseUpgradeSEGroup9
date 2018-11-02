# Greek Life Member Management System

## Set up the system and deploy to a localhost

- Install Python 3 and set up development environment: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/development_environment
- Follow the steps provided in the link.
- When you get to the installation of virtualenvwrapper you may need to use -H in the sudo command to get it to install properly (e.g. sudo **-H** pip3 install virtualenvwrapper)
- Stop after Python is installed.
- To install Crispy-Forms, in the terminal execute the command: pip3 install django-crispy-forms
- Download the databaseUpgradeSEGroup9 repository by selecting the clone or downlod button at the top right of the main GitHub page for the project and select download zip from the choices
- Unzip the file
- In a terminal navigate to the main GLMMS folder (you will know that this is the correct one because it will contain a file named __manage.py__)
- Ensure that your virtual environment is still active and enter the command: python3 manage.py runserver
- Open a browser window and navigate to: http://127.0.0.1:8000/

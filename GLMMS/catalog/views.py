'''this class is only being used to serve the project index page'''
from django.shortcuts import render

def index(request):
    # Render the HTML template index.html 
    return render(
        request,
        'index.html')

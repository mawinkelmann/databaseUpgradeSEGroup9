'''this class is only being used to serve the project index page
Author: Christopher Whetsel

'''

from django.shortcuts import render

def index(request):
    # Render the HTML template index.html 
    return render(
        request,
        'index.html')

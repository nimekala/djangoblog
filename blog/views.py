from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home (request):
    return HttpResponse("<h1>Welcome THe DJango</h1> <p>this is the djamgblog homepage.</p>")

def about (request):
    return render(request, 'blog/home.html', {'content':'this is the djamgblog team.'})

def contact (request):
    return render(request, 'blog/contact.html', {'content':'this is the djamgblog team.'})

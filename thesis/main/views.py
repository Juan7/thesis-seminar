from django.shortcuts import render

# Create your views here.


def home(request):
    """Display home view."""

    context = {
        'text': 'Hello world!',
    }
    return render(request, 'main/home.html', context)

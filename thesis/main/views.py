"""Contain views for main app."""
import json
import pprint

from operator import itemgetter

from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
# Create your views here.

from .functions import differential_evolution, load_init_data

def home(request):
    """Display home view."""
    result_data = request.session.get('result_data', {})

    context = {
        'result_data': result_data,
    }
    return render(request, 'main/home.html', context)


def run(request):
    """Run a new test algorithm."""
    data = load_init_data()
    generations = settings.GENERATIONS or 10
    result_data = differential_evolution(generations, data)

    for result in result_data['generations']:
        result.sort(key=lambda x:x['fitness'][0])
        result = list(reversed(result))

    request.session['result_data'] = result_data
    # pprint.pprint(result_data)
    return redirect(reverse('main:home'))

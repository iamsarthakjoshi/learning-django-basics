from django.shortcuts import render
from django.http import HttpResponse, Http404

from .models import Pet

# Create your views here.

def home(req):
    # return HttpResponse('<p>Home View</p>')
    pets = Pet.objects.all()
    return render(req, 'home.html', {'pets': pets,})

def pet_detail(req, pet_id):
    # return HttpResponse(f'<p>pet_detail view with id {pet_id}</p>')
    try:
        pet = Pet.objects.get(id=pet_id)
    except Pet.DoesNotExit:
        raise Http404('Pet not found!')

    return render(req, 'pet_detail.html', {'pet': pet,})

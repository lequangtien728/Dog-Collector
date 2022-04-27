from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from .forms import FeedingForm
from django.http import HttpResponse # res.send in express
from .models import Dog, Toy # importing our model

# the template the CreateView and the UpdateView use is the same
# templates/<app_name>/<model>_form.html
# templates/main_app/cat_form.html

class DogCreate(CreateView):
    model = Dog
    fields = '__all__' # this include all the fields (name, breed, description, age) on the Dog model in models.py

class DogUpdate(UpdateView):
    model = Dog
    fields =['breed','description','age']

class DogDelete(DeleteView):
    model = Dog
    success_url = '/dogs/'

#Define the home view
def home(request):
    return HttpResponse('<h1>Tien Quang Le</h1>')

def about(request):
    return render(request, 'about.html')

def dogs_index(request):
    dogs = Dog.objects.all()
    return render(request, 'dogs/index.html', {'dogs': dogs})

def dogs_detail(request, dog_id):
  dog = Dog.objects.get(id=dog_id)
  # create an instance of FeedingForm
  feeding_form = FeedingForm()

  return render (request, 'dogs/detail.html', {'dog': dog, 'feeding_form': feeding_form})

def add_feeding(request, dog_id):
  # create a ModelForm instance using the data in request.POST
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the cat_id assigned
    new_feeding = form.save(commit=False)
    new_feeding.dog_id = dog_id
    new_feeding.save() # adds the feeding to the database, and the feeding be associated with the 
  return redirect('detail', dog_id=dog_id)


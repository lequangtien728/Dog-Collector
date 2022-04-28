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
    fields =['breed','description','age'] # because we don't want to let anyone change the dog name, we don't include in the fields.

class DogDelete(DeleteView):
    model = Dog
    success_url = '/dogs/'

#Define the home view
def home(request):
    return HttpResponse('<h1>Tien Quang Le</h1>')

def about(request):
    return render(request, 'about.html')

def dogs_index(request):
    dogs = Dog.objects.all() # using our model to get all the rows in our dog table in PSQL
    return render(request, 'dogs/index.html', {'dogs': dogs})

# path('dogs/<int:dog_id>/' <- this is where dog_id comes from-
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
    new_feeding.save() # adds the feeding to the database, and the feeding be associated with the dog
    # with same id as the argument to the function dog_id 
  return redirect('detail', dog_id=dog_id)

class ToyList(ListView):
    model = Toy

class ToyDetail(DetailView):
    model = Toy

class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'

class ToyUpdate(UpdateView):
    model = Toy
    fields = '__all__' #__all__ mean all the field in Toy model(name and color)

class ToyDelete(DeleteView):
    model = Toy
    success_url= '/toys/'
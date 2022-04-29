from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from .forms import FeedingForm
from django.http import HttpResponse # res.send in express
from .models import Dog, Toy, Photo # importing our model

# the template the CreateView and the UpdateView use is the same
# templates/<app_name>/<model>_form.html
# templates/main_app/dog_form.html

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

import uuid
import boto3
# Add these "constant" variables below the imports
S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'dogcollector511'

def add_photo(request, dog_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to dog_id or dog (if you have a dog object)
            Photo.objects.create(url=url, dog_id=dog_id)
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', dog_id=dog_id)

class DogCreate(CreateView):
    model = Dog
    fields = ['name','breed','description','age'] # this include all the fields (name, breed, description, age) on the Dog model in models.py

    # This inherited method is called when a
    # valid dog form is being submitted
    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the dog
        # Let the CreateView do its job as usual
        return super().form_valid(form)

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
    dogs = Dog.objects.filter(user=request.user) # using our model to get all the rows in our dog table in PSQL
    # You could also retrieve the logged in user's cats like this
    # cats = request.user.cat_set.all()
    return render(request, 'dogs/index.html', {'dogs': dogs})

# path('dogs/<int:dog_id>/' <- this is where dog_id comes from-
def dogs_detail(request, dog_id):
  dog = Dog.objects.get(id=dog_id)
  # Get the toys the Dog doesn't have
  toys_dog_doesnt_have = Toy.objects.exclude(id__in = dog.toys.all().values_list('id'))
  # create an instance of FeedingForm
  feeding_form = FeedingForm()

  return render (request, 'dogs/detail.html', {'dog': dog, 'feeding_form': feeding_form,'toys':toys_dog_doesnt_have})

def add_feeding(request, dog_id):
  # create a ModelForm instance using the data in request.POST
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the Dog_id assigned
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

def associate_toy(request, dog_id, toy_id):
    Dog.objects.get(id=dog_id).toys.add(toy_id)#you can pass toy's id instead of whole object
    return redirect('detail', dog_id=dog_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
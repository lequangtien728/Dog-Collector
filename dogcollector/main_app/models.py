from django.db import models
from django.urls import reverse
from datetime import date

#Import the User
from django.contrib.auth.models import User

#create many to many 
class Toy(models.Model):
  name = models.CharField(max_length=60)
  color = models.CharField(max_length=30)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('toys_detail', kwargs={'pk': self.id})

# Create your models here.
class Dog(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    #add the M:M relationship 
    toys = models.ManyToManyField(Toy)

    # Add the foreign key linking to a user instance
    user = models.ForeignKey(User, on_delete=models.CASCADE) #linking dog to a User
    
    def __str__(self):
        return f"The Dog named {self.name} has id of {self.id}"

    def get_absolute_url(self):
        return reverse('detail', kwargs={'dog_id': self.id})


# A tuple of 2-tuples
MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)


class Feeding(models.Model):
  date = models.DateField('feeding date')
  meal = models.CharField(
    max_length=1,
    # add the 'choices' field option
    choices=MEALS,
    # set the default value for meal to be 'B'
    default=MEALS[0][0]
  )

    #the foreign key always goes on the many side
    #internally it will be dog_id and the _id automatically gets added
    # Create a dog_id FK
  dog = models.ForeignKey(Dog, on_delete=models.CASCADE)

  def __str__(self):
    # Nice method for obtaining the friendly value of a Field.choice
    return f"{self.get_meal_display()} on {self.date}"

  class Meta:
      ordering =['-date']

class Photo(models.Model):
    url = models.CharField(max_length=200)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for dog_id: {self.dog_id} @{self.url}"
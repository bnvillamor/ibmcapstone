from django.db import models
from django.utils.timezone import now


# Create your models here.

# Car Make model
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Add any other fields you'd like for the car make model

    def __str__(self):
        return f"{self.name}"


class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()  # Refers to a dealer in the Cloudant database
    name = models.CharField(max_length=100)
    TYPE_CHOICES = (
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'WAGON'),
        # Add other choices as needed
    )
    car_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    year = models.DateField()
    # Add any other fields you'd like for the car model

    def __str__(self):
        return f"{self.car_make} - {self.name}"
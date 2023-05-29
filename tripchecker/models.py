from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Choices
from django.contrib.auth.models import User
from tripchecker.ninjas_api import set_coordinates



def validate_name(value):
    v = set_coordinates(str(value))

    if v.latitude() is None:
        raise ValidationError("This city is not found. Check your spelling.")
    else:
        return value

class Trips(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200,  validators=[validate_name])
    start = models.DateField()
    end = models.DateField()
    Yes = "Y"
    No = "N"
    VISIT_CHOICES = [(Yes, "Yes"), (No, "No")]
    visited = models.CharField(max_length=3, choices=VISIT_CHOICES, default=VISIT_CHOICES[1])
    description = models.CharField(max_length=200, blank=True)
    longitude = models.FloatField(default=None, null=True, blank=True)
    latitude = models.FloatField(default=None, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Trips"

    def save(self, *args, **kwargs):
        v = set_coordinates(str(self.name))
        self.longitude = v.longitude()
        self.latitude = v.latitude()
        if self.start > self.end:
            raise ValidationError("The dates are incorrect. Check the start and the end of the trip")
        super(Trips, self).save(*args, **kwargs)
    def __str__(self):
        return self.name






from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # ... (other fields)

    def as_dict(self):
        return {
            'id': self.user.id,
            'username': self.user.username,
            'investments': [investment.id for investment in self.user.investment_set.all()],
        }


class Property(models.Model):
    PROPERTY_TYPES = (
        ('AG', 'Agriculture'),
        ('RE', 'Real Estate'),
    )

    property_type = models.CharField(max_length=2, choices=PROPERTY_TYPES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    area = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

class Investment(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    investor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.investor.username} - {self.property.title}"

class Crop(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    yield_per_hectare = models.FloatField()

    def __str__(self):
        return self.name

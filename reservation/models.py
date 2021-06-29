from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm

from car.models import Car


class ShopCart (models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
    from_location = models.CharField( max_length=50, null=True)
    to_location = models.CharField( max_length=50, null=True)
    date = models.CharField( max_length=50, null=True)
    time = models.CharField( max_length=50, null=True)
    distance = models.IntegerField( max_length=50, null=True)

    def __str__(self):
        return self.car.title

    @property
    def calculated_price(self):
        # return self.distance
        # return (self.car.km_price + self.car.base_price)
        return (int(self.distance * self.car.km_price + self.car.base_price))


    @property
    def price(self):
        return self.car.base_price


class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['from_location','to_location', 'date', 'time']


class Reservation(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Waiting', 'Waiting'),
        ('Confirmed', 'Confirmed'),
        ('Canceled', 'Canceled'),
    )

    user_id =  models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    car_id =models.IntegerField(null=False)
    from_location_id =models.IntegerField(null=False)
    to_location_id =models.IntegerField(null=False)
    price = models.FloatField(null=False,default="0")
    airline=models.CharField( max_length=50, null=True)
    flightnumber = models.CharField( max_length=50, null=True)
    flightarrivedate =models.CharField( max_length=50, null=True)
    flightarrivetime =models.CharField( max_length=50, null=True)
    pickuptime =models.CharField( max_length=50, null=True)
    first_name= models.CharField( max_length=50, null=True)
    last_name= models.CharField( max_length=50, null=True)
    phone= models.CharField( max_length=50, null=True)
    code = models.CharField(max_length=5, editable=False, null=True)
    note= models.TextField(null=True)
    ip = models.CharField( max_length=50, null=True)
    status = models.CharField( max_length=50, default='New', choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def __str__(self):
        return self.user.first_name


class ReserveForm(ModelForm):
    class Meta:
        model= Reservation
        fields=['airline','flightnumber','flightarrivedate','flightarrivetime','pickuptime','note']

class ReserveCar(models.Model):
    STATUS= (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Canceled', 'Canceled'),
    )

    reserve = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    car = models.ForeignKey(Car, on_delete= models.CASCADE)
    price = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS, default='New')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.car.title


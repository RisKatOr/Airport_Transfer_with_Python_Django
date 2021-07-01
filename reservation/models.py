from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm
from numpy import number

from car.models import Car


class ShopCart (models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
    from_location = models.CharField( max_length=50, null=True)
    to_location = models.CharField( max_length=50, null=True)
    date = models.CharField( max_length=50, null=True)
    time = models.CharField( max_length=50, null=True)
    distance = models.IntegerField( null=True)

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

class Reserve(models.Model):
    STATUS = (
        ('Waiting', 'Waiting'),
        ('Confirmed', 'Confirmed'),
        ('Canceled', 'Canceled'),
    )

    user= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    car= models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
    code= models.CharField(max_length=5, editable=False)
    first_name= models.CharField(max_length=20)
    last_name= models.CharField(max_length=20)
    phone=models.CharField(blank=True,max_length=20)
    ip=models.CharField(blank=True,max_length=20)
    total = models.FloatField(null=True)
    airline = models.CharField(max_length=50, null=True)
    flightnumber = models.CharField(max_length=50, null=True)
    flightarrivedate = models.CharField(max_length=50, null=True)
    flightarrivetime = models.CharField(max_length=50, null=True)
    adminnote= models.TextField(null=True)
    pickuptime = models.CharField(max_length=50, null=True)
    pickupdate = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=100, null=True)
    note = models.TextField(null=True)
    status=models.CharField(max_length=10, choices=STATUS,default='Waiting')
    created_at = models.DateTimeField(auto_now_add=True ,null=True, blank=True),
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True),

    def __str__(self):
        return self.user.first_name


class ReservationForm(ModelForm):
    class Meta:
        model=Reserve
        fields= ['first_name','last_name','phone','airline','flightnumber','flightarrivedate','flightarrivetime','note','country','address']


class ReserveCar(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Canceled', 'Canceled'),
    )
    reserve= models.ForeignKey(Reserve,on_delete=models.CASCADE)
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    car= models.ForeignKey(Car,on_delete=models.CASCADE)
    price=models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.car.title






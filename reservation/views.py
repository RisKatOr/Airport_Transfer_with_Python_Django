from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
import haversine as hs
from haversine import Unit

from car.models import Category
from reservation.models import ShopCartForm, ShopCart


def index(request):
   return HttpResponse("order App")


@login_required(login_url = '/login')
def addtocart(request, id):
   url = request.META.get('HTTP_REFERER')
   if request.method == 'POST':
      form = ShopCartForm(request.POST)
      if form.is_valid():
         current_user = request.user

         data = ShopCart()
         data.user_id = current_user.id
         data.car_id = id
         fromdata =form.cleaned_data['from_location']
         fromdata = fromdata.split(',')
         fromLatitude= float(fromdata[0])
         fromLongitude=float(fromdata[1])
         fromPlace=fromdata[2]
         data.from_location = fromPlace
         todata = form.cleaned_data['to_location']
         todata = todata.split(',')
         toLatitude = float(todata[0])
         toLongitude = float(todata[1])
         toPlace = todata[2]
         data.to_location = toPlace
         loc1 = (toLatitude, toLongitude)
         loc2 = (fromLatitude, fromLongitude)

         distance = hs.haversine(loc1, loc2, unit=Unit.KILOMETERS)
         data.distance = distance
         # data.to_location =form.cleaned_data['to_location']
         data.date =form.cleaned_data['date']
         data.time =form.cleaned_data['time']
         data.save()

         request.session['cart_items'] = ShopCart.objects.filter(user_id = current_user.id).count() #count items in shop cart

         messages.success( request, "Added to shopping cart.")

         return HttpResponseRedirect(url)


def shopcart(request):
   category = Category.objects.all()
   current_user = request.user
   shopcart = ShopCart.objects.filter(user_id = current_user.id)
   request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()  # count items in shop cart

   total = 0

   # for rs in shopcart:
   #    total+= rs.car.base_price * rs.quantity

   context = {
      'shopcart': shopcart,
      'category': category
   }

   return render(request,'reservation.html',context)

def deletecart(request,id):
   ShopCart.objects.filter(id=id).delete()
   messages.success(request, "Added to shopping cart.")

   return HttpResponseRedirect("/reservation")

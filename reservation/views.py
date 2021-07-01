from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
import haversine as hs
from haversine import Unit
from django.utils.crypto import get_random_string
from car.models import Category, Car
from home.models import UserProfile
from reservation.models import ShopCartForm, ShopCart, ReservationForm, Reserve, ReserveCar


def index(request):
    return HttpResponse("order App")


@login_required(login_url='/login')
def addtocart(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    checkshopcart = ShopCart.objects.filter(user_id=current_user.id)
    car = Car.objects.get(id=id)
    if checkshopcart:
        messages.warning(request, 'You can not add item more than one to shopping cart.Please delete the cart first')
        return HttpResponseRedirect(url)
    else:
        if request.method == 'POST':
            form = ShopCartForm(request.POST)
            if form.is_valid():
                current_user = request.user
                data = ShopCart()
                data.user_id = current_user.id
                data.car_id = id
                fromdata = form.cleaned_data['from_location']
                fromdata = fromdata.split(',')
                fromLatitude = float(fromdata[0])
                fromLongitude = float(fromdata[1])
                fromPlace = fromdata[2]
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
                data.date = form.cleaned_data['date']
                data.time = form.cleaned_data['time']
                data.save()

                # carmodel = Car()
                car.status = 'False'
                car.save()

                request.session['cart_items'] = ShopCart.objects.filter(
                    user_id=current_user.id).count()  # count items in shop cart

                messages.success(request, "Added to shopping cart.")

                return HttpResponseRedirect(url)


def shopcart(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()  # count items in shop cart
    profile = UserProfile.objects.get(user_id=current_user.id)
    form = ReservationForm()
    total = 0

    # for rs in shopcart:
    #    total+= rs.car.base_price * rs.quantity

    context = {
        'shopcart': shopcart,
        'category': category,
        'total': total,
        'form': form,
        'profile': profile,
    }

    return render(request, 'reservation.html', context)


@login_required(login_url='/login')  # Check login
def deletecart(request, id):
    ShopCart.objects.filter(car_id=id).delete()
    car = Car.objects.get(id=id)
    car.status = 'True'
    car.save()
    messages.success(request, "Deleted from shopping cart.")

    return HttpResponseRedirect("/reservation")


@login_required(login_url='/login')  # Check login
def bookcar(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.get(user_id=current_user.id)
    total = 0
    total += shopcart.car.base_price + shopcart.car.km_price * shopcart.distance
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():

            data = Reserve()
            data.first_name = form.cleaned_data['first_name']  # get product quantity from form
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.note = form.cleaned_data['note']
            data.airline = form.cleaned_data['airline']
            data.flightnumber = form.cleaned_data['flightnumber']
            data.flightarrivedate = form.cleaned_data['flightarrivedate']
            data.flightarrivetime = form.cleaned_data['flightarrivetime']
            data.country = form.cleaned_data['country']
            data.address = form.cleaned_data['address']
            data.total = total
            data.user_id = current_user.id

            data.ip = request.META.get('REMOTE_ADDR')
            detail = ReserveCar()
            detail.reserve_id = data.id  # Order Id
            detail.car_id = shopcart.car_id
            detail.user_id = current_user.id
            detail.distance = shopcart.distance
            ordercode = get_random_string(5).upper()  # random cod
            data.from_location = shopcart.from_location
            data.to_location = shopcart.to_location
            data.pickupdate = shopcart.date
            data.pickuptime = shopcart.time
            data.car_id = shopcart.car_id
            data.code = ordercode
            data.save()
            ShopCart.objects.get(user_id=current_user.id).delete()  # Clear & Delete shopcart
            request.session['cart_items'] = 0
            messages.success(request, "Your Order has been completed. Thank you ")
            return render(request, 'reservation_complated.html', {'ordercode': ordercode, 'category': category})

        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/reservation/")
    form = ReservationForm()
    profile= UserProfile.objects.get(user_id= current_user.id)
    context = {
        'shopcart': shopcart,
        'category': category,
        'total': total,
        'form': form,
        'profile': profile,
    }
    return HttpResponseRedirect(request,'reservation.html',context)


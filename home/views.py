from django.contrib import messages
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from car.models import Car, Category, Images, Comment
from django.contrib.auth import logout

from home.forms import SignUpForm
from home.models import Setting, ContactForm, ContactFormMessage, UserProfile, FAQ
from django.contrib.auth import authenticate, login

from reservation.models import ShopCart


def index(request):
    current_user = request.user
    setting = Setting.objects.get(pk=1)
    sliderdata = Car.objects.all()[:4]
    category = Category.objects.all()
    daycar = Car.objects.all()[:3]
    lastcar = Car.objects.all().order_by('id')[:3]
    randomcar = Car.objects.all().order_by('?')[:3]
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()  # count items in shop cart

    context = {'setting': setting,
               'page':'home',
               'sliderdata': sliderdata,
               'category': category,
               'daycar':daycar,
               'lastcar': lastcar,
               'randomcar': randomcar,
               }

    return render(request, 'index.html', context)

def aboutus(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    category = Category.objects.all()
    context = {'setting': setting, 'page':'aboutus','category': category}
    # the reason why we used 'page' is we can use a if operation if we need
    return render(request, 'aboutus.html', context)

def references(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()

    context = {'setting': setting, 'page':'references','category': category}
    # the reason why we used 'page' is we can use a if operation if we need
    return render(request, 'references.html', context)

def contact(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactFormMessage() #connection between model and form
            data.name =form.cleaned_data['name']
            data.email =form.cleaned_data['email']
            data.subject =form.cleaned_data['subject']
            data.ip =request.META.get('REMOTE_ADDR')
            data.message =form.cleaned_data['message']
            data.save() #save to database
            messages.success(request, "We got your message successfully and we will turn back you soon.. Thank you! :)")
            return HttpResponseRedirect('/contact')

    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    form= ContactForm()
    context = {'setting': setting, 'form': form,'category': category}
    # the reason why we used 'page' is we can use a if operation if we need
    return render(request, 'contact.html', context)

def category_cars(request, id,slug):

    category = Category.objects.all()
    categorydata = Category.objects.get(pk= id)
    cars= Car.objects.filter(category_id = id, status='True')
    context = {'cars': cars,
               'category': category,
               'categorydata': categorydata,

               }
    # the reason why we used 'page' is we can use a if operation if we need
    return render(request, 'cars.html', context)


def car_detail(request,id,slug):
    category = Category.objects.all()
    car = Car.objects.get(pk=id)
    images= Images.objects.filter(car=id)
    comments= Comment.objects.filter(car=id, status='True')

    context = {
                'car': car,
                'images': images,
               'category': category,
               'comments': comments,

               }

    return render(request, 'car_detail.html',context)

def car_search(request):
    if request.method == 'POST':
        from home.forms import SearchForm
        form= SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']
            filter = form.cleaned_data['filter']

            if filter == 0:
                cars = Car.objects.filter(title__icontains = query) #select * from car where title like %query%

            else:
                cars = Car.objects.filter(title__icontains=query, category_id= filter)
            context = {
                'cars': cars,
                'category': category,
            }
        return render(request, 'car_search.html', context)

    return HttpResponseRedirect('/')


def car_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        car = Car.objects.filter(title__icontains=q)
        results = []
        for rs in car:
            car_json = {}
            car_json = rs.title
            results.append(car_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            userprofile = UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage'] = userprofile.image.url
            return HttpResponseRedirect('/')

        else:
            # Return an 'invalid login' error message.
            messages.warning(request, "Wrong username or password !")
            return HttpResponseRedirect('/login')
    category = Category.objects.all()
    context = {

        'category': category,


    }
    return render(request, 'login.html', context)

def join_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()  # completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            # Create data in profile table for user
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/Profile.jpg" #boş gelmesi durumunda hata almamak için default bir  değer atamışız gibi düşünebiliriz
            data.save()
            messages.success(request, 'Your account has been created!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/join')

    form = SignUpForm()
    category = Category.objects.all()
    context = {
        'category': category,
        'form': form,
    }
    return render(request, 'join.html', context)

def faq(request):
    category = Category.objects.all()
    faq = FAQ.objects.all().order_by('ordernumber')
    context = {
        'category': category,
        'faq': faq,
    }
    return render(request,'faq.html',context)

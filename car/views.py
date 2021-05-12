from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from car.models import CommentForm, Comment


def index(request):
    text="Don't be panic "
    context = {'text': text}
    return render(request, 'index.html', context)

@login_required(login_url='/login') #check login
def addcomment(request,id):
    url = request.META.get('HTTP_REFERER')  # get last url
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            current_user =request.user #access user session informations

            data = Comment() #connection with model
            data.user_id = current_user.id
            data.car_id = id
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request,"Your review sent successfully. Thank you!")

            return  HttpResponseRedirect(url)

    messages.warning(request, "ERROR ! There is something wrong. please fill out all sections or try again !  ")

    return HttpResponseRedirect(url)


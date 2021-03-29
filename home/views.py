from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting, ContactForm, ContactFormMessage


def index(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page':'home'}
    return render(request, 'index.html', context)

def aboutus(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page':'aboutus'}
    # the reason why we used 'page' is we can use a if operation if we need
    return render(request, 'aboutus.html', context)

def references(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page':'references'}
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
    form= ContactForm()
    context = {'setting': setting, 'form': form}
    # the reason why we used 'page' is we can use a if operation if we need
    return render(request, 'contact.html', context)

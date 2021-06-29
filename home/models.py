from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
from django.forms import ModelForm, TextInput, Textarea
from django.utils.safestring import mark_safe



class Setting(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    status = models.CharField(max_length=10, choices=STATUS)
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    company = models.CharField(max_length=50)
    address = models.CharField(blank=True,max_length=100)
    phone = models.CharField(blank=True,max_length=100)
    fax = models.CharField(blank=True,max_length=30)
    email = models.CharField(blank=True,max_length=30)
    smtpserver = models.CharField(blank=True,max_length=20)
    smtpemail = models.CharField(blank=True,max_length=10)
    smtppassword = models.CharField(blank=True,max_length=30)
    smtpport = models.CharField(blank=True,max_length=5)
    facebook = models.CharField(blank=True,max_length=50)
    instagram = models.CharField(blank=True,max_length=50)
    twitter = models.CharField(blank=True,max_length=50)
    aboutus = RichTextField()
    contact = RichTextField()
    references = RichTextField()
    icon= models.ImageField(blank=True, upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ContactFormMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Not Solved', 'Not Solved'),
        ('Solved', 'Solved'),
    )
    name= models.CharField(blank=True, max_length=20)
    email= models.CharField(blank=True, max_length=50)
    subject= models.CharField(blank=True, max_length=50)
    message= models.CharField(blank=True, max_length=500)
    status= models.CharField(max_length=10, choices=STATUS, default='New')
    ip=models.CharField(blank=True,max_length=20)
    note=models.CharField(blank=True,max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ContactForm(ModelForm):
    class Meta:
        model = ContactFormMessage
        fields= ['name','email','subject','message']
        widgets = {
            'name' : TextInput(attrs={'class': 'form-control' , 'placeholder' : 'Name & Surname'}),
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'subject' : TextInput(attrs={'class': 'form-control' , 'placeholder' : 'Subject'}),
            'message' : Textarea(attrs={'class': 'form-control' , 'placeholder' : 'Message','rows':'5'}),
        }

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=30, blank=True)
    image = models.ImageField(blank=True, upload_to='images/users/')
    def __str__(self):
        return self.user.username

    def first_name(self):
        return self.user.first_name + ' ' +self.user.last_name

    def user_name(self):
        return self.user.username

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields= ['phone','address','city','country' ,'image']

class FAQ(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    status = models.CharField(max_length=10, choices=STATUS)
    question = models.CharField(max_length=150)
    answer = models.TextField()
    ordernumber = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question
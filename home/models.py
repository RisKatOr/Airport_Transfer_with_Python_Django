from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

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
    address = models.CharField(blank=True,max_length=30)
    phone = models.CharField(blank=True,max_length=30)
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


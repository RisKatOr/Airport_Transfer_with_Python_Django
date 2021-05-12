from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from ckeditor.fields import RichTextField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    detail = RichTextField()
    status = models.CharField(max_length=10, choices=STATUS)
    image = models.ImageField(blank=True, upload_to='images/')
    slug = models.SlugField(max_length =50, null = True, blank = False)
    parent= models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['title']



    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'


class Car(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    status = models.CharField(max_length=10, choices=STATUS)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    detail = RichTextField()
    description = models.CharField(max_length=30)
    keywords = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    slug = models.SlugField(max_length =50, null = True, blank = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.title


    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'


class Images(models.Model):
    car= models.ForeignKey(Car, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')
    def __str__(self):
        return self.title


class Comment(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),
        ('New', 'Yeni'),
    )
    status = models.CharField(max_length=10, choices=STATUS)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    comment = models.TextField(max_length=200)
    rate = models.IntegerField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS,default='New')
    ip = models.CharField(blank=True,max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject','comment','rate']

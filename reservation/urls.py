from django.urls import path

from . import views

urlpatterns = [
    # ex: /home/
    path('', views.index, name='index'),
    path('addtocart/<int:id>',views.addtocart, name = 'addtocart'),
    path('deletecart/<int:id>',views.deletecart, name = 'deletecart'),
    path('bookcar/', views.bookcar, name='bookcar'),
]
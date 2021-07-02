from django.contrib import admin

# Register your models here.
from reservation.models import ShopCart,Reserve,ReserveCar

class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['user', 'car', 'from_location', 'to_location', 'calculated_price']
    list_filter =  ['user']

class ReserveCarline(admin.TabularInline):
    model = ReserveCar
    readonly_fields = ('user','car','price')
    can_delete = False
    extra = 0

class ReserveAdmin(admin.ModelAdmin):

    list_display = ['first_name','last_name','pickupdate','pickuptime','total','status']
    list_filter = ['status']
    readonly_fields = ('user','phone','first_name','last_name','phone','total','ip','car','airline','flightnumber','flightarrivedate','flightarrivetime', 'pickuptime','pickupdate','country','address','note')
    inlines = [ReserveCarline]
    can_delete = False

class ReserveCarAdmin(admin.ModelAdmin):
    list_display = ['user','car','price','status']
    list_filter = ['user']

admin.site.register(ShopCart,ShopCartAdmin)
admin.site.register(Reserve,ReserveAdmin)
admin.site.register(ReserveCar,ReserveCarAdmin)


from ast import Add
from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,SuperAgent,HOD,BookPlot,AddPlot,Customer,Fundtransfer,Installment,phase


# Register your models here.

# class UserModel(UserAdmin):
#     list_display = ['username', 'user_type']


# class UserModel(UserAdmin):
#     pass

admin.site.register(CustomUser)
admin.site.register(SuperAgent)
admin.site.register(HOD)
admin.site.register(BookPlot)
admin.site.register(AddPlot)
admin.site.register(Customer)
admin.site.register(Fundtransfer)
admin.site.register(Installment)
admin.site.register(phase)

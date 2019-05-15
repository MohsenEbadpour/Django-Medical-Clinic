from django.contrib import admin

# Register your models here.
from .models import User,Sick,Doctor,Staff
class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = Sick
class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = User
class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = Doctor

class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = Staff

admin.site.register(User,UserAdmin)
admin.site.register(Doctor,UserAdmin)
admin.site.register(Sick,UserAdmin)
admin.site.register(Staff,UserAdmin)
from django.contrib import admin
from .models import Turn,Shift
# Register your models here.
class TurnAdmin(admin.ModelAdmin):
    class Meta:
        model = Turn
class ShiftAdmin(admin.ModelAdmin):
    class Meta:
        model = Shift
        
admin.site.register(Turn,TurnAdmin)
admin.site.register(Shift,ShiftAdmin)
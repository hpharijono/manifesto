from django.contrib import admin
from .models import Value, Principle

class ValueAdmin(admin.ModelAdmin):
    pass


class PrincipleAdmin(admin.ModelAdmin):
    pass


# Register your models here.
admin.site.register(Value, ValueAdmin)
admin.site.register(Principle, PrincipleAdmin)
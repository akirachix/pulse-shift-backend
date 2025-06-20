from django.contrib import admin

# Register your models here.
from .models import Customer, MamaMboga, Address

admin.site.register(Customer)
admin.site.register(MamaMboga)
admin.site.register(Address)
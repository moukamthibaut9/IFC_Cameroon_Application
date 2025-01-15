from django.contrib import admin
from .models import Company,Convention,Setting,Employee,Folder

# Register your models here.
admin.site.register(Company)
admin.site.register(Convention)
admin.site.register(Setting)
admin.site.register(Employee)
admin.site.register(Folder)

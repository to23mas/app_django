from django.contrib import admin
from .models import Ukol, Soubor, Project, UserAccount

admin.site.register(Ukol)
admin.site.register(Soubor)
admin.site.register(Project)
admin.site.register(UserAccount)

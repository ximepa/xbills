# -*- encoding: utf-8 -*-
from django.contrib import admin
from .models import ClientUr, TelUr


class ClientUrAdmin(admin.ModelAdmin):
    pass


class TelUrAdmin(admin.ModelAdmin):
    pass

admin.site.register(ClientUr, ClientUrAdmin)
admin.site.register(TelUr, TelUrAdmin)
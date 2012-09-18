# coding: utf-8
from django.contrib import admin
from shipping.models import (Zone, Country, State, UPSCarrier, CorreiosCarrier, Package)


class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')
    list_filter = ('status', )


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso', 'status')
    list_filter = ('zone', 'status')
    search_fields = ('name', )


class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    list_filter = ('country__zone', )
    search_fields = ('name', 'country__name')


admin.site.register(Zone, ZoneAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(UPSCarrier)
admin.site.register(CorreiosCarrier)
admin.site.register(Package)

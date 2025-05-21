from django.contrib import admin

from .models import *

@admin.register(Lliga)
class LligaAdmin(admin.ModelAdmin):
    list_display = ('nom', 'temporada', 'data_inici', 'data_fi')
    search_fields = ('nom', 'temporada')

@admin.register(Equip)
class EquipAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ciutat', 'fundacio')
    search_fields = ('nom', 'ciutat')

@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin):
    list_display = ('nom', 'cognoms', 'dorsal', 'posicio', 'equip')
    search_fields = ('nom', 'cognoms', 'equip__nom')
    list_filter = ('posicio', 'nacionalitat')
    autocomplete_fields = ['equip']

class EventInline(admin.TabularInline):
    model = Event
    fields = ["temps", "tipus", "jugador", "equip", "detalls"]
    ordering = ("temps",)
    extra = 1

@admin.register(Partit)
class PartitAdmin(admin.ModelAdmin):
    search_fields = ["local__nom", "visitant__nom", "lliga__nom"]
    readonly_fields = ["resultat"]
    list_display = ["local", "visitant", "resultat", "lliga", "data", "finalitzat"]
    list_filter = ("lliga", "finalitzat", "data")
    ordering = ("-data",)
    inlines = [EventInline]
    autocomplete_fields = ['lliga', 'local', 'visitant']

    def resultat(self, obj):
        gols_local = obj.events.filter(tipus="GOL", equip=obj.local).count()
        gols_visit = obj.events.filter(tipus="GOL", equip=obj.visitant).count()
        return f"{gols_local} - {gols_visit}"

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('partit', 'temps', 'tipus', 'jugador', 'equip')
    list_filter = ('tipus', 'equip', 'partit__lliga')
    search_fields = ('jugador__nom', 'jugador__cognoms', 'equip__nom')
    autocomplete_fields = ['partit', 'jugador', 'equip']
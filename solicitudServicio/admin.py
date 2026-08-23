from django.contrib import admin

# Register your models here.
from .models import Pedido, Servicio

admin.site.site_header = "Admon HogarLimpio"
admin.site.site_title = "Panel HogarLimpio"
admin.site.index_header = "Control de Operaciones"

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio', 'categoria', 'disponible')
    list_filter = ('categoria', 'disponible')
    search_fields = ('nombre',)

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente_nombre', 'estado', 'total', 'fecha')
    list_filter = ('estado', 'fecha')
    search_fields = ('cliente_nombre',)
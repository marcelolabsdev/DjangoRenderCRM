from django.contrib import admin
from .models import Empresa, Contacto, Oportunidad, Actividad


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sector', 'sitio_web')
    search_fields = ('nombre', 'sector')
    list_filter = ('sector',)


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono', 'empresa', 'estado', 'fecha_creacion')
    search_fields = ('nombre', 'email', 'empresa__nombre')
    list_filter = ('estado', 'empresa')
    list_per_page = 25


@admin.register(Oportunidad)
class OportunidadAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'valor', 'etapa', 'contacto', 'empresa', 'fecha_cierre_estimada')
    search_fields = ('titulo', 'contacto__nombre', 'empresa__nombre')
    list_filter = ('etapa',)
    list_per_page = 25


@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'contacto', 'fecha', 'descripcion')
    search_fields = ('contacto__nombre', 'descripcion')
    list_filter = ('tipo',)
    list_per_page = 25

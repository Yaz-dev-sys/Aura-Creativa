from django.contrib import admin
from .models import info

@admin.register(info)
class InfoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'empresa_proyecto', 'servicio', 'id')
    list_filter = ('servicio',)
    search_fields = ('nombre', 'email', 'empresa_proyecto')
    readonly_fields = ('id',)
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'email')
        }),
        ('Información del Proyecto', {
            'fields': ('empresa_proyecto', 'servicio', 'descripcion')
        }),
    )
    
    def has_delete_permission(self, request, obj=None):
        # Opcional: controlar si se puede eliminar desde el admin
        return True
    
    def has_change_permission(self, request, obj=None):
        # Opcional: controlar si se puede editar desde el admin
        return True
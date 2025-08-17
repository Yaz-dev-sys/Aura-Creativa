from django.db import models


class info(models.Model):
    SERVICIOS_CHOICES = [
        ('branding', 'Branding & Identidad'),
        ('web', 'Desarrollo Web'),
        ('marketing', 'Marketing Digital'),
        ('content', 'Creación de Contenido'),
        ('all', 'Proyecto integral'),
    ]

    nombre = models.CharField(max_length=250, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    empresa_proyecto = models.CharField(max_length=250, verbose_name="Empresa / Proyecto", null=False, blank=False)
    servicio = models.CharField(max_length=50, null=False, blank=False, choices=SERVICIOS_CHOICES)
    descripcion = models.TextField(null=False, blank=False)

    def __str__(self):
        return f"{self.nombre} - {self.servicio}"
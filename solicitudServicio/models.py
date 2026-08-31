from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.
#Django ORM - Crear

def validar_precio_positivo(value):
    if value <= 0:
        raise ValidationError('El precio debe ser un número mayor a cero.')
    
class Pedido(models.Model):
    CATEGORIAS = [
        ('COMPLETA', 'Completa'),
        ('EXPRESS', 'Express'),
        ('EXTERIORES', 'Exteriores'),
    ]
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    categoria = models.CharField(max_length=10, choices=CATEGORIAS)
    disponible = models.BooleanField(default=True)

# Soporte para archivos multimedia (Media Files)
#    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

class Servicio(models.Model):
    ESTADOS = [
        ('ACTIVO', 'Activo'),
        ('CANCELADO', 'Cancelado'),
        ('ACEPTADO', 'Aceptado'),
        ('RECHAZADO', 'Rechazado'),
        ('EN PROCESO', 'En proceso'),
        ('TERMINADO', 'Terminado'),
        ('PENDIENTE', 'Pendiente')
    ]
    SERVICIO = [
        ('CASA', 'Casa'),
        ('DEPARTAMENTO', 'Departamento'),
        ('OFICINA', 'Oficina'),
    ]
    cliente_nombre = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    servicio = models.CharField(max_length=15, choices=SERVICIO, default='PENDIENTE')
    estado = models.CharField(max_length=15, choices=ESTADOS, default='PENDIENTE')
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Orden #{self.id} - {self.cliente_nombre} ({self.estado})"
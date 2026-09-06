from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.
#Django ORM - Crear

def validar_precio_positivo(value):
    if value <= 0:
        raise ValidationError('El precio debe ser un número mayor a cero.')
    
class Servicio(models.Model):
    CATEGORIAS = [
        ('COMPLETO', 'Completo'),
        ('EXPRESS', 'Express'),
        ('EXTERIORES', 'Exteriores'),
    ]
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    categoria = models.CharField(max_length=15, choices=CATEGORIAS, default= 'COMPLETO')
    disponible = models.BooleanField(default=True)

# Soporte para archivos multimedia (Media Files)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

class Pedido(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('ACEPTADO', 'Aceptado'),
        ('RECHAZADO', 'Rechazado'),
        ('EN PROCESO', 'En proceso'),
        ('TERMINADO', 'Terminado'),
        ('CANCELADO', 'Cancelado'),        
    ]
    
    cliente_nombre = models.CharField(max_length=100)
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT, related_name='pedidos')
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='PENDIENTE')
    disponible = models.BooleanField(default=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Orden #{self.id} - {self.cliente_nombre} ({self.estado})"
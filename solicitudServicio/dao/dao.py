from typing import List, Optional
from solicitudServicio.models import Pedido, Servicio

class PedidoDAO:
    """Capa DAO para solicitudes de Pedidos"""
    
    @staticmethod
    def obtener_todos() -> List[Pedido]:
        return Pedido.objects.all().order_by('-fecha')

    @staticmethod
    def obtener_disponibles() -> List[Pedido]:
        return Pedido.objects.filter(disponible=True).order_by('-fecha')

    @staticmethod
    def obtener_por_id(pedido_id: int) -> Optional[Pedido]:
        try:
            return Pedido.objects.get(id=pedido_id)
        except Pedido.DoesNotExist:
            return None
        
    @staticmethod
    def crear_pedido_con_servicio(cliente_nombre: str, servicio_id: int) -> Optional[Pedido]:
        try:
            servicio = Servicio.objects.get(
            id=servicio_id,
            disponible=True
            )
            pedido = Pedido.objects.create(
            cliente_nombre=cliente_nombre,
            servicio=servicio,
            total=servicio.precio
            )   
            return pedido
        except Servicio.DoesNotExist:
         return None
    
    @staticmethod
    def cambiar_estado(pedido_id: int, nuevo_estado: str) -> Optional[Pedido]:
            try:
                pedido = Pedido.objects.get(id=pedido_id)
                pedido.estado = nuevo_estado
                pedido.save()  # Ejecuta la consulta UPDATE en la BD
                return pedido
            except Pedido.DoesNotExist:
                return None

class ServicioDAO:
    """Capa DAO para operaciones de Servicio"""

    @staticmethod
    def obtener_todos() -> List[Servicio]:
        return Servicio.objects.all()

    @staticmethod
    def obtener_disponibles() -> List[Servicio]:
        return Servicio.objects.filter(disponible=True)
       
    
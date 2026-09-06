from django.shortcuts import render, redirect
# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib import messages

from solicitudServicio.dao.dao import ServicioDAO, PedidoDAO
from solicitudServicio.serializers import ServicioSerializer, PedidoSerializer
from django.contrib.auth.decorators import login_required, user_passes_test
# ==========================================
# Roles
# ==========================================
def es_pedidos(user):
    """Verifica si el usuario autenticado pertenece al grupo 'Pedidos' o es Staff/Admin"""
    return user.is_authenticated and (user.groups.filter(name='pedidos').exists() or user.is_staff)

# ==========================================
# 1. VISTAS WEB (HTML)
# ==========================================

def menu_view(request):
    """Muestra el catálogo de servicios al cliente utilizando el DAO"""
    servicios = ServicioDAO.obtener_disponibles()
    return render(request, 'mainvista/menu.html', {'servicios': servicios})

@login_required # type: ignore
@user_passes_test(es_pedidos, login_url='/admin/login/') # type: ignore
def pedidos_view(request):
    """Muestra los pedidos activos"""
    # Consulta solo pedidos activos con el nuevo metodo del DAO
    pedidos_activos = PedidoDAO.obtener_pendientes_o_en_proceso()
    return render(request, 'mainvista/pedidos.html', {'pedidos': pedidos_activos})

def crear_pedido_action(request):
    """Procesa el formulario web de un nuevo pedido."""

    if request.method == 'POST':
        cliente_nombre = request.POST.get('cliente_nombre','').strip()
        servicio_id = request.POST.get('servicio_id')
        if cliente_nombre and servicio_id:
            try:
                servicio_id = int(servicio_id)
                pedido = PedidoDAO.crear_pedido_con_servicio(cliente_nombre,servicio_id)
                if pedido:
                    messages.success(request,f"¡Pedido registrado a nombre de {cliente_nombre}!")
                else:
                    messages.error(request,"El servicio no existe o no está disponible.")
            except (ValueError, TypeError):
                messages.error(request,"El servicio seleccionado no es válido.")
        else:
            messages.error(request,"Por favor ingresa tu nombre y selecciona un servicio.")
    return redirect('menu')

@login_required
@user_passes_test(es_pedidos, login_url='/admin/login/')
def cambiar_estado_action(request, pedido_id):
    """Actualiza el estado del pedido desde la vista web"""
    if request.method == 'POST':
        nuevo_estado = request.POST.get('nuevo_estado')
        PedidoDAO.cambiar_estado(pedido_id, nuevo_estado)
    return redirect('pedidos')

# ==========================================
# 2. VISTAS API REST (JSON)
# ==========================================

class ServicioViewSet(viewsets.ViewSet):
    """API para consultar servicios disponibles"""
    def list(self, request):
        servicios = ServicioDAO.obtener_todos()
        serializer = ServicioSerializer(servicios, many=True)
        return Response(serializer.data)

class PedidoViewSet(viewsets.ViewSet):
    #Permite listar los pedidos (GET)
    def list(self, request):
        pedidos = PedidoDAO.obtener_todos()
        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data)

    # Permite crear un pedido desde la API (POST)
    def create(self, request):
        cliente_nombre = request.data.get('cliente_nombre')
        servicio_id = request.data.get('servicio_id')

        if not cliente_nombre or not servicio_id:
            return Response(
                {"error": "Se requieren cliente_nombre y servicio_id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        pedido = PedidoDAO.crear_pedido_con_servicio(cliente_nombre, int(servicio_id))
        if pedido:
            serializer = PedidoSerializer(pedido)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            {"error": "Producto no encontrado o no disponible"},
            status=status.HTTP_404_NOT_FOUND
        )
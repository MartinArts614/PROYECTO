from django.test import TestCase
from django.urls import reverse
from solicitudServicio.models import Servicio, Pedido
from solicitudServicio.dao.dao import ServicioDAO, PedidoDAO


class HogarLimpioTestCase(TestCase):
    def setUp(self):
        self.servicio = Servicio.objects.create(
            nombre="Servicio primera vez",
            precio=500.00,
            categoria="COMPLETO",
            disponible=True
        )

    def test_crear_pedido(self):
        pedido = PedidoDAO.crear_pedido_con_servicio("Alfonso", self.servicio.id)
        self.assertIsNotNone(pedido)
        self.assertEqual(pedido.cliente_nombre, "Alfonso")
        self.assertEqual(pedido.total, 500.00)
        self.assertEqual(pedido.servicio, self.servicio)

    def test_cambiar_estado_dao(self):
        pedido = PedidoDAO.crear_pedido_con_servicio("Ana", self.servicio.id)
        self.assertIsNotNone(pedido)
        pedido_actualizado = PedidoDAO.cambiar_estado(pedido.id, "EN PROCESO")
        self.assertIsNotNone(pedido_actualizado)
        self.assertEqual(pedido_actualizado.estado, "EN PROCESO")

## para probar los endpoint rest, verifica que la api nos responda 
    def test_api_list_servicios(self):
        response = self.client.get('/api/productos/')
        self.assertEqual(response.status_code, 200)

    def test_crear_pedido_action_web(self):
        response = self.client.post(reverse('crear_pedido'), {
            'cliente_nombre': 'Antonio',
            'servicio_id': self.servicio.id
        })
        self.assertRedirects(response, reverse('menu'))
        self.assertEqual(Pedido.objects.count(), 1)
        pedido = Pedido.objects.first()
        self.assertEqual( pedido.cliente_nombre, 'Antonio' )
        self.assertEqual( pedido.servicio, self.servicio )
        self.assertEqual( pedido.total, 500.00 )

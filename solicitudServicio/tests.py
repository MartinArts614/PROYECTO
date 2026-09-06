from django.test import TestCase
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Servicio, Pedido

class SmokeTests(TestCase):
    def setUp(self):
        """Configuración de datos iniciales para la prueba"""
        self.servicio = Servicio.objects.create(
            nombre="Servicio primera vez",
            precio=250.00,
            categoria="COMPLETO",
            disponible=True
        )
        self.user = User.objects.create_superuser(
            username='admin_test',
            email='admin@test.com',
            password='password123'
        )

    def test_creacion_servicio(self):
        """Verifica que el producto se guarde correctamente en la base de datos"""
        self.assertEqual(Servicio.objects.count(), 1)
        self.assertEqual(self.servicio.nombre, "Servicio primera vez")
        self.assertEqual(self.servicio.precio, 250.00)
        self.assertEqual(self.servicio.categoria, "COMPLETO")
        self.assertTrue(self.servicio.disponible)

    def test_creacion_pedido(self):
        """Verifica la creación de un pedido asociado a un cliente y producto"""
        pedido = Pedido.objects.create(
            cliente_nombre="Juana de Arco",
            servicio=self.servicio,
            estado="PENDIENTE",
            total=250.00
        )
        self.assertEqual(Pedido.objects.count(), 1)
        self.assertEqual(pedido.cliente_nombre, "Juana de Arco")
        self.assertEqual(pedido.servicio, self.servicio)
        self.assertEqual(pedido.estado, "PENDIENTE")
        self.assertEqual(pedido.total, 250.00)

    def test_acceso_admin_importar_csv(self):
        """Verifica que la vista del cargue masivo responda correctamente (HTTP 200)"""
        self.client.login(username='admin_test', password='password123')
        response = self.client.get('/admin/solicitudServicio/servicio/importar-csv/')
        self.assertEqual(response.status_code, 200)
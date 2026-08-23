#Serializer conversion de datos a JSON
from rest_framework import serializers
from solicitudServicio.models import Servicio, Pedido

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
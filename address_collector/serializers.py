from rest_framework import serializers
from address_collector.models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'address', 'latitude', 'longitude',
                  'created_on', 'updated_on')

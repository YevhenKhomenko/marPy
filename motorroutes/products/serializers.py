from rest_framework import serializers
from .models import Product, Manufacturer


class ManufacturerNestedSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField() 
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'description']
        
    
class ProductListSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Product
        fields = ['id', 'name', 'description']

    
class ProductDetailsSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturerNestedSerializer()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'vendor_code', 'manufacturer', 'created_by']
        
    def update(self, instance, validated_data):
        manufacturer_data = validated_data.pop('manufacturer')
        instance = super().update(instance, validated_data)
        manufacturer = Manufacturer.objects.get(pk=manufacturer_data.get('id'))
        instance.manufacturer = manufacturer
        instance.save()
        return instance

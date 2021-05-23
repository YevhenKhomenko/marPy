from rest_framework import serializers
from .models import Product, Manufacturer
from django.shortcuts import get_object_or_404


class ManufacturerNestedSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField() 
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'description']

   
class FanufacturerValidationMixIn():
    def validate_manufacturer(self, data):
        m_count = Manufacturer.objects.filter(id=data.get('id')).count()
        if m_count == 1:
            return data
        else:
            raise serializers.ValidationError("wrong Manufacturer id")

        return data

    
class ProductListSerializer(serializers.ModelSerializer, FanufacturerValidationMixIn):
    manufacturer = ManufacturerNestedSerializer()
        
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'manufacturer', 'created_on']

        
    def create(self, validated_data):
        manufacturer_data = validated_data.pop('manufacturer')
        instance = super().create(validated_data)
        manufacturer = get_object_or_404(Manufacturer, id=manufacturer_data.get('id'))# get object or 404
        instance.manufacturer = manufacturer
        instance.save()
        return instance
        

class ProductDetailsSerializer(serializers.ModelSerializer, FanufacturerValidationMixIn):
    manufacturer = ManufacturerNestedSerializer()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'vendor_code', 'manufacturer', 'created_by']  

            
    def update(self, instance, validated_data):
        manufacturer_data = validated_data.pop('manufacturer')
        instance = super().update(instance, validated_data)
        manufacturer = get_object_or_404(Manufacturer, id=manufacturer_data.get('id'))# get object or 404
        instance.manufacturer = manufacturer
        instance.save()
        return instance
        


'''
{
    "id": 3,
    "name": "q2",
    "description": "123123",
    "vendor_code": 123,
    "manufacturer": {
        "id": 123
    },
    "created_by": 1
}
'''

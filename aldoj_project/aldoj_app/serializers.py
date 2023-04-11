from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Property, Investment, Crop

class UserSerializer(serializers.ModelSerializer):
    investments = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'investments']

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'title', 'description', 'property_type', 'location', 'area', 'price']

class InvestmentSerializer(serializers.ModelSerializer):
    property = PropertySerializer(read_only=True)
    investor = serializers.StringRelatedField()

    class Meta:
        model = Investment
        fields = ['id', 'amount', 'date', 'property', 'investor']

class CropSerializer(serializers.ModelSerializer):
    property = PropertySerializer()

    class Meta:
        model = Crop
        fields = ['id', 'name', 'yield_per_hectare', 'property']

from rest_framework import serializers
from .models import outputa

class outputSerializer(serializers.ModelSerializer):

    class Meta:
        model = outputa
        fields = '__all__'
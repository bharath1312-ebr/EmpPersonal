from rest_framework import serializers
from .models import EmpPersonal

class EmpSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpPersonal
        fields = ("name", "email", "age", "mobile", "address", "country")
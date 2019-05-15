from django.contrib.auth.models import User, Group
from .models import Student
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ['id', 'user', 'last_modified_date']

    def create(self, validated_data):
        return Student.objects.create(**validated_data)

# class StudentSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     last_modified_date = serializers.DateTimeField()

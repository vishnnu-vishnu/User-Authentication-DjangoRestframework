from rest_framework import serializers
from userapp.models import RegisterDB


class userserializer(serializers.ModelSerializer):
    class Meta:
        id=serializers.CharField(read_only=True)
        password=serializers.CharField(write_only=True)
        model = RegisterDB
        fields = [
            'name',
            'email',
            'password',
            'is_verified'
        ]


class loginserializer(serializers.ModelSerializer):
    class Meta:
        model=RegisterDB
        email=serializers.EmailField()
        password=serializers.CharField(write_only=True)
        fields=[
            'email',
            'password'
        ]

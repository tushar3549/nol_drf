from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email','first_name','last_name','phone','avatar','language','currency']
class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['username','email','password']
    def create(self, data):
        u=User(username=data.get('username'), email=data.get('email'))
        u.set_password(data['password'])
        u.save(); return u
class LoginSerializer(serializers.Serializer):
    username=serializers.CharField(); password=serializers.CharField(write_only=True)
    def validate(self, attrs):
        user=authenticate(username=attrs['username'], password=attrs['password'])
        if not user: raise serializers.ValidationError('Invalid credentials')
        attrs['user']=user; return attrs

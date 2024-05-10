from rest_framework import serializers
from pos_app.models import (User, TableResto, Category, MenuResto, OrderMenu, OrderMenuDetail, Profile)
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class TableRestoSerializer(serializers.ModelSerializer):
    model = TableResto
    fields = ('id', 'code', 'name', 'capacity', 'table_status', 'status')

class RegisterUserSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
  password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
  password2 = serializers.CharField(write_only=True, required=True)

  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2', 'is_active', 'is_waitress', 'first_name', 'last_name']
    extra_kwargs = {
      'first_name': {'required': True}, 
      'last_name': {'required': True},
    }

  def validate(self, attrs):
      if attrs['password1'] != attrs['password2']:
          raise serializers.ValidationError({
              'password': "Passwords don't match. Please try again!"
          })
      return attrs
    
  def create(self, validated_data):
    user = User.objects.create(
        username=validated_data['username'],
        email=validated_data['email'],
        is_active=validated_data.get('is_active', False),
        is_waitress=validated_data.get('is_waitress', False),
        first_name=validated_data['first_name'],
        last_name=validated_data['last_name']
    )
    user.set_password(validated_data['password1'])
    user.save()
    return user
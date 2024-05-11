from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from pos_app.models import (User, TableResto, StatusModel, Profile, Category, MenuResto, OrderMenu, OrderMenuDetail)
from api.serializers import (TableRestoSerializer, RegisterUserSerializer, LoginSerializer, MenuRestoSerializer) # ProfileSerializer, ProfileSerializerII, CategorySerializer, StatusModelSerializer, UserSerializer
from rest_framework import generics
from rest_framework.authtoken.models import Token
from django.contrib.auth import login as django_login, logout as django_logout
from django.http import JsonResponse, HttpResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .paginators import CustomPagination

class TableRestoListApiView(APIView):
  # method get
  def get(self, request, *args, **kwargs):
    table_restos = TableResto.objects.all()
    serializer = TableRestoSerializer(table_restos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  # method post
  def post(self, request, *args, **kwargs):
    data = {
      'code': request.data.get('code'),
      'name': request.data.get('name'),
      'capacity': request.data.get('capacity'),
    }
    serializer = TableRestoSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      response = {
        'status': status.HTTP_201_CREATED,
        'message': 'Data created successfully',
        'data': serializer.data
      }
      return Response(response, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class TableRestoDetailApiView(APIView):
  # method to get specific data
  def get_object(self, id):
    try:
      return TableResto.objects.get(id=id)
    except TableResto.DoesNotExist:
      return None
    
  def get(self, request, *args, **kwargs):
    table_resto_instance = self.get_object(self.kwargs['id'])
    if not table_resto_instance:
      return Response(
        {
          'status': status.HTTP_404_NOT_FOUND,
          'message': 'Data not found',
          'data': {}
        }, status=status.HTTP_404_NOT_FOUND
      )
    
    serializer = TableRestoSerializer(table_resto_instance)
    response = {
      'status': status.HTTP_200_OK,
      'message': 'Data retrieved successfully',
      'data': serializer.data
    }
    return Response(response, status=status.HTTP_200_OK)
    
  # method to update data
  def put(self, request, *args, **kwargs):
    table_resto_instance = self.get_object(self.kwargs['id'])
    if not table_resto_instance:
      return Response(
        {
          'status': status.HTTP_404_NOT_FOUND,
          'message': 'Data not found',
          'data': {}
        }, status=status.HTTP_404_NOT_FOUND
      )
    
    data = {
      'code': request.data.get('code'),
      'name': request.data.get('name'),
      'capacity': request.data.get('capacity'),
      'table_status': request.data.get('table_status'),
      'status': request.data.get('status'),
    }
    serializer = TableRestoSerializer(instance=table_resto_instance, data=data, partial=True)
    if serializer.is_valid():
      serializer.save()
      response = {
        'status': status.HTTP_200_OK,
        'message': 'Data updated successfully',
        'data': serializer.data
      }
      return Response(response, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  # method DELETE
  def delete(self, request, id, *args, **kwargs):
    table_resto_instance = self.get_object(id)
    if not table_resto_instance:
      return Response(
        {
          'status': status.HTTP_400_BAD_REQUEST,
          'message': 'Data not found',
          'data': {}
        }, status=status.HTTP_400_BAD_REQUEST
      )
    
    table_resto_instance.delete()
    response = {
      'status': status.HTTP_200_OK,
      'message': 'Data deleted successfully',
    }
    return Response(response, status=status.HTTP_200_OK)
  
class RegisterUserAPIView(APIView):
  serializer_class = RegisterUserSerializer
  
  def post(self, request, format = None):
    serializer = self.serializer_class(data = request.data)
    if serializer.is_valid(): 
      serializer.save()
      response_data = {
        'status': status.HTTP_201_CREATED,
        'message': 'Selamat anda berhasil register',
        'data': serializer.data
      }
      return Response(response_data, status=status.HTTP_201_CREATED)
    return Response({
      'status': status.HTTP_400_BAD_REQUEST,
      'data': serializer.errors
    }, status = status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
  serializer_class = LoginSerializer

  def post(self, request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    django_login(request, user)
    token, created = Token.objects.get_or_create(user=user)
    return JsonResponse({
      'status': 200,
      'message': 'Login success',
      'data': {
        'token': token.key,
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'is_active': user.is_active,
        'is_waitress': user.is_waitress
      }
    })

class MenuRestoView(APIView):
  authentication_classes = [SessionAuthentication, BasicAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self, request, *args, **kwargs):
    menu_restos = MenuResto.objects.select_related('status').filter(status = StatusModel.objects.first())
    serializer = MenuRestoSerializer(menu_restos, many=True)
    response = {
      'status': status.HTTP_200_OK,
      'message': 'Data sucessfully read',
      'user': str(request.user),
      'auth': str(request.auth),
      'data': serializer.data,
    }
    return Response(response, status=status.HTTP_200_OK)

class MenuRestoFilterApi(generics.ListAPIView):
  queryset = MenuResto.objects.all()
  serializer_class = MenuRestoSerializer
  pagination_class = CustomPagination
  permission_classes = [permissions.IsAuthenticated]
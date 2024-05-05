from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from pos_app.models import TableResto
from api.serializers import TableRestoSerializer

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
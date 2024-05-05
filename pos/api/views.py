from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from pos_app.models import TableResto
from api.serializers import TableRestoSerializer

class TableRestoListApiView(APIView):

  def get(self, request, *args, **kwargs):
    table_restos = TableResto.objects.all()
    serializer = TableRestoSerializer(table_restos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
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
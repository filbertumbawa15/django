from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from pos_app.models import User, TableResto
from api.serializers import TableRestoSerializer
from pprint import pprint


class TableRestoListApiView(APIView):

    def get_object(self, id):
        try:
            return TableResto.objects.get(id=id)
        except TableResto.DoesNotExist:
            return None

    def get(self, request, id, *args, **kwargs):
        table_resto_instance = TableResto.objects.get(id)
        if not table_resto_instance:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Data does not exist...',
                    'data': {},
                }, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = TableRestoSerializer(table_resto_instance)
        response = {
            'status': status.HTTP_200_OK,
            'message': 'Data retrieve successfully',
            'data': serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)
        # table_restos = TableResto.objects.all()
        # serializer = TableRestoSerializer(table_restos, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)

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
                'message': "Data Created successfully...",
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, *args, **kwargs):
        table_resto_instance = self.get_objects(id)
        if not table_resto_instance:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Data does not exist...',
                    'data': {}
                }, status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'code': request.data.get('code'),
            'name': request.data.get('name'),
            'capacity': request.data.get('capacity'),
            'table_status': request.data.get('table_status'),
            'status': request.data.get('status'),
        }
        serializer = TableRestoSerializer(
            instance=table_resto_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': status.HTTP_200_OK,
                'message': 'Data updated successfully',
                'data': serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK),
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        table_resto_instance = self.get_object(id)
        if not table_resto_instance:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Data does not exist...',
                'data': {},
            }, status=status.HTTP_400_BAD_REQUEST)

        table_resto_instance.delete()
        response = {
            'status': status.HTTP_201_CREATED,
            'message': "Data Deleted Successfully...",
        }
        return Response(response, status=status.HTTP_200_OK)

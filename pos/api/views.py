from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from pos_app.models import (
    User, TableResto, Profile, Category,
    )
from api.serializers import (
    TableRestoSerializer, LoginSerializer, ProfileSerializer, RegisterWaitressSerializer,
    CategorySerializer
    )
from pprint import pprint
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import login as django_login, logout as django_logout
from django.http import HttpResponse, JsonResponse

# Class  TableRestoListApiView untuk GET all data dan POST
class TableRestoListApiView(APIView):    

    def get(self, request, *args, **kwargs):
        table_restos = TableResto.objects.all()
        serializer = TableRestoSerializer(table_restos, many = True)
        response = {
            'status' : status.HTTP_200_OK,
            'message' : 'Retrive all data success...',
            'data' : serializer.data
        }
        return Response(response, status = status.HTTP_200_OK)
        # return Response(serializer.data, status = status.HTTP_200_OK)       

    def post(self, request, *args,**kwargs):
        data = {
            'code' : request.data.get('code'),
            'name' : request.data.get('name'),
            'capacity' : request.data.get('capacity'),            
        }
        serializer = TableRestoSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_201_CREATED,
                'message' : 'Data created successfully...',
                'data' : serializer.data
            }
            return Response(response, status = status.HTTP_201_CREATED)            

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

# classs TableRestoDetaiilApiView untuk  GET single data, PUT dan DELETE
class TableRestoDetailApiView(APIView):

    # Method dibawah ini digunakan utk mendapatkan object instance dari model tsb
    # Sama dengan spt di ORM Django cth : TableResto.objects.get(id = 1)
    # hasilnya berupa object.
    def get_object(self, id):
        try:
            return TableResto.objects.get(id=id)
        except TableResto.DoesNotExist:
            return None

    # Method dibawah ini digunakan utk mencari data berdasarkan id
    # Hasil ny berupa queryset.
    # Sama dengan mencari method response GET mencari data berdasarkan id
    def get(self, request, id, *args, **kwargs):
        table_resto_instance = self.get_object(id)
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

    # def post(self, request, *args, **kwargs):
    #     data = {
    #         'code': request.data.get('code'),
    #         'name': request.data.get('name'),
    #         'capacity': request.data.get('capacity'),
    #     }
    #     serializer = TableRestoSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         response = {
    #             'status': status.HTTP_201_CREATED,
    #             'message': "Data Created successfully...",
    #             'data': serializer.data
    #         }
    #         return Response(response, status=status.HTTP_201_CREATED)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    
class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        django_login(request, user)
        token, created = Token.objects.get_or_create(user = user)
        return JsonResponse({
            'data' : {
                'token' : token.key,
                'id' : user.id,
                'username' : user.username,
                'first_name' : user.first_name,
                'last_name' : user.last_name,
                'email' : user.email,
                'is_active' : user.is_active,
                # 'is_superuser' : user.is_superuser,
                'is_waitress' : user.is_waitress,
            }, 
            'status' : 200,
            'message' : "You're login right now..."
        })
    
class LogoutView(APIView):
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        django_logout(request)
        # return Response(status=204)
        return JsonResponse({'message': "You have been logout..."})

class RegisterWaitressApi(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterWaitressSerializer

#Start Controller Profile
class ProfileDetailAPI(APIView):
    def get_object(self, user_id):
        try:
            return Profile.objects.get(user = user_id)
        except Profile.DoesNotExist:
            return None
        
    def get(self, request, user_id, *args, **kwargs):
        profile_instance = self.get_object(user_id)
        if not profile_instance:
            return Response(
                {'response': "Data does not exists..."},
                status = status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ProfileSerializer(profile_instance)
        return Response(serializer.data, status = status.HTTP_200_OK)
# End Controller Profile

class CategoryListApiView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
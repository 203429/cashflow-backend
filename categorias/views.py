# Recursos Rest Framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from categorias.models import categoryModel
from categorias.serializers import categorySerializer

from django.db.models import Q

# Others imports
import json

class categoryViewAll(APIView):
    def custom_response(self, msg, response, status):
        data ={
            "messages": msg,
            "pay_load": response,
            "status": status,
        }
        res= json.dumps(data)
        response = json.loads(res)
        return response

    def get(self, request, format=None):
        queryset = categoryModel.objects.all()
        serializer = categorySerializer(queryset , many=True, context={'request':request})
        return Response(self.custom_response("Success", serializer.data, status=status.HTTP_200_OK))

    def post(self, request):
        serializer = categorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(self.custom_response("Success", serializer.data, status=status.HTTP_201_CREATED))
        return Response(self.custom_response("Error", serializer.errors, status=status.HTTP_400_BAD_REQUEST))

class categoryEntradaView(APIView):
    def custom_response(self, msg, response, status):
        data ={
            "messages": msg,
            "pay_load": response,
            "status": status,
        }
        res= json.dumps(data)
        response = json.loads(res)
        return response

    def get(self, request, format=None):
        queryset = categoryModel.objects.filter(categoria="Ingreso").values()
        serializer = categorySerializer(queryset , many=True, context={'request':request})
        return Response(self.custom_response("Success", serializer.data, status=status.HTTP_200_OK))

class categorySalidaView(APIView):
    def custom_response(self, msg, response, status):
        data ={
            "messages": msg,
            "pay_load": response,
            "status": status,
        }
        res= json.dumps(data)
        response = json.loads(res)
        return response

    def get(self, request, format=None):
        queryset = categoryModel.objects.filter(Q(categoria="Costo-Venta") | Q(categoria="Gasto-AOC")).values()
        serializer = categorySerializer(queryset , many=True, context={'request':request})
        return Response(self.custom_response("Success", serializer.data, status=status.HTTP_200_OK))

class categoryViewDetail(APIView):
    def custom_response(self, msg, response, status):
        data ={
            "messages": msg,
            "pay_load": response,
            "status": status,
        }
        res= json.dumps(data)
        response = json.loads(res)
        return response

    def get_object(self, pk):
        try:
            return categoryModel.objects.get(pk=pk)
        except categoryModel.DoesNotExist:
            return 0

    def get(self, request, pk, format=None):
        category = self.get_object(pk)
        if category != 0:
            category = categorySerializer(category)
            return Response(self.custom_response("Success", category.data, status=status.HTTP_200_OK))
        return Response(self.custom_response("Error", "No hay datos", status=status.HTTP_400_BAD_REQUEST))

    def put(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = categorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(self.custom_response("Success", serializer.data, status=status.HTTP_200_OK))
        return Response(self.custom_response("Error", serializer.errors, status = status.HTTP_400_BAD_REQUEST))
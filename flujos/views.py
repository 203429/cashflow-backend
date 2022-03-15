# Recursos Rest Framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from flujos.models import flujoModel
from flujos.serializers import flujoSerializer

from categorias.models import categoryModel

# Others imports
import json

class flujoViewAll(APIView):
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
        queryset = flujoModel.objects.all()
        serializer = flujoSerializer(queryset , many=True, context={'request':request})
        return Response(self.custom_response("Success", serializer.data, status=status.HTTP_200_OK))

    def post(self, request):
        serializer = flujoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(self.custom_response("Success", serializer.data, status=status.HTTP_201_CREATED))
        return Response(self.custom_response("Error", serializer.errors, status=status.HTTP_400_BAD_REQUEST))

class flujoViewDetail(APIView):
    def custom_response(self, msg, response, status):
        data ={
            "messages": msg,
            "pay_load": response,
            "status": status,
        }
        res= json.dumps(data)
        response = json.loads(res)
        return response

    def custom_response_get(self, flujo, categoria):
        data = {
            "flujo": flujo,
            "categoria": {
                "idCategoria":categoria[0]['id'],
                "clasificación":categoria[0]['clasificacion'],
                "categoria":categoria[0]['categoria'],
                "subcategoria":categoria[0]['subcategoria']
            }
        }
        res= json.dumps(data)
        response = json.loads(res)
        return response

    def get_flujo(self, pk):
        try:
            return flujoModel.objects.get(pk=pk)
        except flujoModel.DoesNotExist:
            return 0

    def get(self, request, pk, format=None):
        flujo = self.get_flujo(pk)
        if flujo != 0:
            flujo = flujoSerializer(flujo)
            idCat = flujo.data.get('categoria')
            categoria = categoryModel.objects.filter(id=idCat).values()
            return Response(self.custom_response_get(flujo.data, categoria))
        return Response(self.custom_response("Error", "No hay datos", status=status.HTTP_400_BAD_REQUEST))
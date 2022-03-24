# Recursos Rest Framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Recursos locales
from indicadores.models import indicadorModel
from indicadores.serializers import indicadorSerializer

# Recursos extras
import json

class indicadorViewAll(APIView):
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
        queryset = indicadorModel.objects.all()
        serializer = indicadorSerializer(queryset , many=True, context={'request':request})
        return Response(self.custom_response("Success", serializer.data, status=status.HTTP_200_OK))

    def post(self, request):
        serializer = indicadorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(self.custom_response("Success", serializer.data, status=status.HTTP_201_CREATED))
        return Response(self.custom_response("Error", serializer.errors, status=status.HTTP_400_BAD_REQUEST))

class indicadorViewDetail(APIView):
    def custom_response(self, msg, response, status):
        data ={
            "messages": msg,
            "pay_load": response,
            "status": status,
        }
        res= json.dumps(data)
        response = json.loads(res)
        return response

    def get_indicador(self, pk):
        try:
            return indicadorModel.objects.get(pk=pk)
        except indicadorModel.DoesNotExist:
            return 0

    def delete(self, request, pk, format=None):
        indicador = self.get_indicador(pk)
        if indicador != 0:
            indicador.delete()
            return Response(self.custom_response("Success", "Eliminado", status=status.HTTP_200_OK))
        return Response(self.custom_response("Error", "No se ha podido eliminar", status=status.HTTP_400_BAD_REQUEST))
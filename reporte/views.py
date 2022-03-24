# Recursos Rest Framework
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response

# Recursos locales
from flujos.models import flujoModel
from flujos.serializers import flujoSerializer
from categorias.models import categoryModel

from indicadores.models import indicadorModel
from indicadores.serializers import indicadorSerializer

from array import *
import json
from django.db.models import Q

class reporteFlujoSalidaView(APIView):
    def custom_response_get(self, response):
        res= json.dumps(response)
        response = json.loads(res)

        listResponse = []

        for i in range(len(response[0])):
            finalData={
                "Salida": response[0][i],
                "Semana1" : response[1][i][0],
                "Semana2" : response[1][i][1],
                "Semana3" : response[1][i][2],
                "Semana4" : response[1][i][3],
                "Total" : response[1][i][4],
            }
            listResponse.append(finalData)

        return listResponse

    def get(self, request, format=None):
        flujo = flujoModel.objects.all()
        serializerFlujo = flujoSerializer(flujo , many=True, context={'request':request})
        res= json.dumps(serializerFlujo.data)
        response = json.loads(res)

        fSalida = []            # Resultado final
        subcategoriasS = []     # Subcategorias listado unico
        fechaS = []             # Fechas en base a la posición de subcategorias
        cantidadS = []          # Cantidad

        for i in response:

            if i['tipo']=="Salida":

                catS = i['categoria']
                categoria = categoryModel.objects.filter(id=catS).values()
                subcategoriaRes = categoria[0]['subcategoria']
                if subcategoriaRes in subcategoriasS:
                    xample = 1
                else:
                    subcategoriasS.append(subcategoriaRes)
        
        contadorS = 0
        tamanio = len(subcategoriasS)
        
        for i in range(tamanio):
            categoria = categoryModel.objects.filter(subcategoria=subcategoriasS[contadorS]).values()
            flujo = flujoModel.objects.filter(categoria=categoria[0]['id']).values()
            n = len(flujo)
            temp1 = []
            temp2 = []
            temp3 = []
            temp4 = []
            tempCont = 1
            for j in range(n):
                f1 = flujo[j]['fecha']
                cantida = flujo[j]['cantidad']
                cantidad = str(cantida)
                if n==1:
                    if tempCont==1:
                        temp1a=[]
                        temp1a.append(f1+"-"+cantidad)
                        temp1.insert(0,temp1a)
                if n==2:
                    if tempCont==1:
                        temp2a=[]
                        temp2a.append(f1+"-"+cantidad)
                        temp2.insert(0,temp2a)
                    if tempCont==2:
                        temp2b=[]
                        temp2b.append(f1+"-"+cantidad)
                        temp2.insert(1,temp2b)
                    tempCont+=1
                if n==3:
                    if tempCont==1:
                        temp3a=[]
                        temp3a.append(f1+"-"+cantidad)
                        temp3.insert(0,temp3a)
                    if tempCont==2:
                        temp3b=[]
                        temp3b.append(f1+"-"+cantidad)
                        temp3.insert(1,temp3b)
                    if tempCont==3:
                        temp3c=[]
                        temp3c.append(f1+"-"+cantidad)
                        temp3.insert(2,temp3c)
                    tempCont+=1
                if n==4:
                    if tempCont==1:
                        temp4a=[]
                        temp4a.append(f1+"-"+cantidad)
                        temp4.insert(0,temp4a)
                    if tempCont==2:
                        temp4b=[]
                        temp4b.append(f1+"-"+cantidad)
                        temp4.insert(1,temp4b)
                    if tempCont==3:
                        temp4c=[]
                        temp4c.append(f1+"-"+cantidad)
                        temp4.insert(2,temp4c)
                    if tempCont==4:
                        temp4d=[]
                        temp4d.append(f1+"-"+cantidad)
                        temp4.insert(3,temp4d)
                    tempCont+=1
            if len(temp1)!=0:
                fechaS.insert(contadorS,temp1)
            if len(temp2)!=0:
                fechaS.insert(contadorS,temp2)
            if len(temp3)!=0:
                fechaS.insert(contadorS,temp3)
            if len(temp4)!=0:
                fechaS.insert(contadorS,temp4)
            contadorS+=1
        
        contTemp = 0
        for i in range(len(fechaS)):
            cantidadObjeto = []
            contS1 = 0
            contS2 = 0
            contS3 = 0
            contS4 = 0
            for j in range(len(fechaS[i])):
                temp = fechaS[i][j]
                fecha1 = temp[0].split("-")
                cantidad1 = fecha1[3]
                cantFinal = int(cantidad1)
                fecha = int(fecha1[0])
                if fecha<8:
                    contS1+=cantFinal
                if fecha>7 and fecha<15:
                    contS2+=cantFinal
                if fecha>14 and fecha<22:
                    contS3+=cantFinal
                if fecha>21 and fecha<32:
                    contS4+=cantFinal
            finalCont = contS1 + contS2 + contS3 + contS4
            cantidadObjeto.append(contS1)
            cantidadObjeto.append(contS2)
            cantidadObjeto.append(contS3)
            cantidadObjeto.append(contS4)
            cantidadObjeto.append(finalCont)
            cantidadS.insert(contTemp,cantidadObjeto)
            contTemp+=1

        fSalida.append(subcategoriasS)
        fSalida.append(cantidadS)

        return Response(self.custom_response_get(fSalida))

class reporteFlujoEntradaView(APIView):
    def custom_response_get(self, response):
        res= json.dumps(response)
        response = json.loads(res)

        listResponse = []

        for i in range(len(response[0])):
            finalData={
                "Salida": response[0][i],
                "Semana1" : response[1][i][0],
                "Semana2" : response[1][i][1],
                "Semana3" : response[1][i][2],
                "Semana4" : response[1][i][3],
                "Total" : response[1][i][4],
            }
            listResponse.append(finalData)

        return listResponse

    def get(self, request, format=None):
        flujo = flujoModel.objects.all()
        serializerFlujo = flujoSerializer(flujo , many=True, context={'request':request})
        res= json.dumps(serializerFlujo.data)
        response = json.loads(res)

        fSalida = []            # Resultado final
        subcategoriasS = []     # Subcategorias listado unico
        fechaS = []             # Fechas en base a la posición de subcategorias
        cantidadS = []          # Cantidad

        for i in response:

            if i['tipo']=="Entrada":

                catS = i['categoria']
                categoria = categoryModel.objects.filter(id=catS).values()
                subcategoriaRes = categoria[0]['subcategoria']
                if subcategoriaRes in subcategoriasS:
                    xample = 1
                else:
                    subcategoriasS.append(subcategoriaRes)
        
        contadorS = 0
        tamanio = len(subcategoriasS)
        
        for i in range(tamanio):
            categoria = categoryModel.objects.filter(subcategoria=subcategoriasS[contadorS]).values()
            flujo = flujoModel.objects.filter(categoria=categoria[0]['id']).values()
            n = len(flujo)
            temp1 = []
            temp2 = []
            temp3 = []
            temp4 = []
            tempCont = 1
            for j in range(n):
                f1 = flujo[j]['fecha']
                cantida = flujo[j]['cantidad']
                cantidad = str(cantida)
                if n==1:
                    if tempCont==1:
                        temp1a=[]
                        temp1a.append(f1+"-"+cantidad)
                        temp1.insert(0,temp1a)
                if n==2:
                    if tempCont==1:
                        temp2a=[]
                        temp2a.append(f1+"-"+cantidad)
                        temp2.insert(0,temp2a)
                    if tempCont==2:
                        temp2b=[]
                        temp2b.append(f1+"-"+cantidad)
                        temp2.insert(1,temp2b)
                    tempCont+=1
                if n==3:
                    if tempCont==1:
                        temp3a=[]
                        temp3a.append(f1+"-"+cantidad)
                        temp3.insert(0,temp3a)
                    if tempCont==2:
                        temp3b=[]
                        temp3b.append(f1+"-"+cantidad)
                        temp3.insert(1,temp3b)
                    if tempCont==3:
                        temp3c=[]
                        temp3c.append(f1+"-"+cantidad)
                        temp3.insert(2,temp3c)
                    tempCont+=1
                if n==4:
                    if tempCont==1:
                        temp4a=[]
                        temp4a.append(f1+"-"+cantidad)
                        temp4.insert(0,temp4a)
                    if tempCont==2:
                        temp4b=[]
                        temp4b.append(f1+"-"+cantidad)
                        temp4.insert(1,temp4b)
                    if tempCont==3:
                        temp4c=[]
                        temp4c.append(f1+"-"+cantidad)
                        temp4.insert(2,temp4c)
                    if tempCont==4:
                        temp4d=[]
                        temp4d.append(f1+"-"+cantidad)
                        temp4.insert(3,temp4d)
                    tempCont+=1
            if len(temp1)!=0:
                fechaS.insert(contadorS,temp1)
            if len(temp2)!=0:
                fechaS.insert(contadorS,temp2)
            if len(temp3)!=0:
                fechaS.insert(contadorS,temp3)
            if len(temp4)!=0:
                fechaS.insert(contadorS,temp4)
            contadorS+=1
        
        contTemp = 0
        for i in range(len(fechaS)):
            cantidadObjeto = []
            contS1 = 0
            contS2 = 0
            contS3 = 0
            contS4 = 0
            for j in range(len(fechaS[i])):
                temp = fechaS[i][j]
                fecha1 = temp[0].split("-")
                cantidad1 = fecha1[3]
                cantFinal = int(cantidad1)
                fecha = int(fecha1[0])
                if fecha<8:
                    contS1+=cantFinal
                if fecha>7 and fecha<15:
                    contS2+=cantFinal
                if fecha>14 and fecha<22:
                    contS3+=cantFinal
                if fecha>21 and fecha<32:
                    contS4+=cantFinal
            finalCont = contS1 + contS2 + contS3 + contS4
            cantidadObjeto.append(contS1)
            cantidadObjeto.append(contS2)
            cantidadObjeto.append(contS3)
            cantidadObjeto.append(contS4)
            cantidadObjeto.append(finalCont)
            cantidadS.insert(contTemp,cantidadObjeto)
            contTemp+=1

        fSalida.append(subcategoriasS)
        fSalida.append(cantidadS)

        return Response(self.custom_response_get(fSalida))

class reporteIndicadorCPC(APIView):
    def custom_response_get(self, response):
        res= json.dumps(response)
        response = json.loads(res)

        listResponse = []

        for i in range(len(response[0])):
            finalData={
                "Salida": response[0][i],
                "Semana1" : response[1][i][0],
                "Semana2" : response[1][i][1],
                "Semana3" : response[1][i][2],
                "Semana4" : response[1][i][3],
                "Total" : response[1][i][4],
            }
            listResponse.append(finalData)

        return listResponse

    def get(self, request, format=None):
        indicador = indicadorModel.objects.all()
        serizalicerIndicador = indicadorSerializer(indicador , many=True, context={'request':request})
        res= json.dumps(serizalicerIndicador.data)
        response = json.loads(res)

        fSalida = []            # Resultado final
        subcategoriasS = []     # Tipo CPC (Cuenta por Cobrar) - CPP (Cuentas por Pagar) - BNC (Bancos)
        fechaS = []             # Fechas en base a la posición de subcategorias
        cantidadS = []          # Cantidad

        for i in response:

            if i['tipo']=="CPC":

                # catS = i['categoria']
                # categoria = categoryModel.objects.filter(id=catS).values()
                subcategoriaRes = i['razon']
                if subcategoriaRes in subcategoriasS:
                    xample = 1
                else:
                    subcategoriasS.append(subcategoriaRes)
        
        contadorS = 0
        tamanio = len(subcategoriasS)
        
        for i in range(tamanio):
            # categoria = categoryModel.objects.filter(subcategoria=subcategoriasS[contadorS]).values()
            # flujo = flujoModel.objects.filter(categoria=categoria[0]['id']).values()
            indicador = indicadorModel.objects.filter(Q(tipo="CPC") & Q(razon=subcategoriasS[contadorS])).values()
            n = len(indicador)
            temp1 = []
            temp2 = []
            temp3 = []
            temp4 = []
            tempCont = 1
            for j in range(n):
                f1 = indicador[j]['fecha']
                cantida = indicador[j]['cantidad']
                cantidad = str(cantida)
                if n==1:
                    if tempCont==1:
                        temp1a=[]
                        temp1a.append(f1+"-"+cantidad)
                        temp1.insert(0,temp1a)
                if n==2:
                    if tempCont==1:
                        temp2a=[]
                        temp2a.append(f1+"-"+cantidad)
                        temp2.insert(0,temp2a)
                    if tempCont==2:
                        temp2b=[]
                        temp2b.append(f1+"-"+cantidad)
                        temp2.insert(1,temp2b)
                    tempCont+=1
                if n==3:
                    if tempCont==1:
                        temp3a=[]
                        temp3a.append(f1+"-"+cantidad)
                        temp3.insert(0,temp3a)
                    if tempCont==2:
                        temp3b=[]
                        temp3b.append(f1+"-"+cantidad)
                        temp3.insert(1,temp3b)
                    if tempCont==3:
                        temp3c=[]
                        temp3c.append(f1+"-"+cantidad)
                        temp3.insert(2,temp3c)
                    tempCont+=1
                if n==4:
                    if tempCont==1:
                        temp4a=[]
                        temp4a.append(f1+"-"+cantidad)
                        temp4.insert(0,temp4a)
                    if tempCont==2:
                        temp4b=[]
                        temp4b.append(f1+"-"+cantidad)
                        temp4.insert(1,temp4b)
                    if tempCont==3:
                        temp4c=[]
                        temp4c.append(f1+"-"+cantidad)
                        temp4.insert(2,temp4c)
                    if tempCont==4:
                        temp4d=[]
                        temp4d.append(f1+"-"+cantidad)
                        temp4.insert(3,temp4d)
                    tempCont+=1
            if len(temp1)!=0:
                fechaS.insert(contadorS,temp1)
            if len(temp2)!=0:
                fechaS.insert(contadorS,temp2)
            if len(temp3)!=0:
                fechaS.insert(contadorS,temp3)
            if len(temp4)!=0:
                fechaS.insert(contadorS,temp4)
            contadorS+=1
        
        contTemp = 0
        for i in range(len(fechaS)):
            cantidadObjeto = []
            contS1 = 0
            contS2 = 0
            contS3 = 0
            contS4 = 0
            for j in range(len(fechaS[i])):
                temp = fechaS[i][j]
                fecha1 = temp[0].split("-")
                cantidad1 = fecha1[3]
                cantFinal = int(cantidad1)
                fecha = int(fecha1[0])
                if fecha<8:
                    contS1+=cantFinal
                if fecha>7 and fecha<15:
                    contS2+=cantFinal
                if fecha>14 and fecha<22:
                    contS3+=cantFinal
                if fecha>21 and fecha<32:
                    contS4+=cantFinal
            finalCont = contS1 + contS2 + contS3 + contS4
            cantidadObjeto.append(contS1)
            cantidadObjeto.append(contS2)
            cantidadObjeto.append(contS3)
            cantidadObjeto.append(contS4)
            cantidadObjeto.append(finalCont)
            cantidadS.insert(contTemp,cantidadObjeto)
            contTemp+=1

        fSalida.append(subcategoriasS)
        fSalida.append(cantidadS)

        return Response(self.custom_response_get(fSalida))

class reporteIndicadorCPP(APIView):
    def custom_response_get(self, response):
        res= json.dumps(response)
        response = json.loads(res)

        listResponse = []

        for i in range(len(response[0])):
            finalData={
                "Salida": response[0][i],
                "Semana1" : response[1][i][0],
                "Semana2" : response[1][i][1],
                "Semana3" : response[1][i][2],
                "Semana4" : response[1][i][3],
                "Total" : response[1][i][4],
            }
            listResponse.append(finalData)

        return listResponse

    def get(self, request, format=None):
        indicador = indicadorModel.objects.all()
        serizalicerIndicador = indicadorSerializer(indicador , many=True, context={'request':request})
        res= json.dumps(serizalicerIndicador.data)
        response = json.loads(res)

        fSalida = []            # Resultado final
        subcategoriasS = []     # Tipo CPC (Cuenta por Cobrar) - CPP (Cuentas por Pagar) - BNC (Bancos)
        fechaS = []             # Fechas en base a la posición de subcategorias
        cantidadS = []          # Cantidad

        for i in response:

            if i['tipo']=="CPP":

                # catS = i['categoria']
                # categoria = categoryModel.objects.filter(id=catS).values()
                subcategoriaRes = i['razon']
                if subcategoriaRes in subcategoriasS:
                    xample = 1
                else:
                    subcategoriasS.append(subcategoriaRes)
        
        contadorS = 0
        tamanio = len(subcategoriasS)
        
        for i in range(tamanio):
            # categoria = categoryModel.objects.filter(subcategoria=subcategoriasS[contadorS]).values()
            # flujo = flujoModel.objects.filter(categoria=categoria[0]['id']).values()
            indicador = indicadorModel.objects.filter(Q(tipo="CPP") & Q(razon=subcategoriasS[contadorS])).values()
            n = len(indicador)
            temp1 = []
            temp2 = []
            temp3 = []
            temp4 = []
            tempCont = 1
            for j in range(n):
                f1 = indicador[j]['fecha']
                cantida = indicador[j]['cantidad']
                cantidad = str(cantida)
                if n==1:
                    if tempCont==1:
                        temp1a=[]
                        temp1a.append(f1+"-"+cantidad)
                        temp1.insert(0,temp1a)
                if n==2:
                    if tempCont==1:
                        temp2a=[]
                        temp2a.append(f1+"-"+cantidad)
                        temp2.insert(0,temp2a)
                    if tempCont==2:
                        temp2b=[]
                        temp2b.append(f1+"-"+cantidad)
                        temp2.insert(1,temp2b)
                    tempCont+=1
                if n==3:
                    if tempCont==1:
                        temp3a=[]
                        temp3a.append(f1+"-"+cantidad)
                        temp3.insert(0,temp3a)
                    if tempCont==2:
                        temp3b=[]
                        temp3b.append(f1+"-"+cantidad)
                        temp3.insert(1,temp3b)
                    if tempCont==3:
                        temp3c=[]
                        temp3c.append(f1+"-"+cantidad)
                        temp3.insert(2,temp3c)
                    tempCont+=1
                if n==4:
                    if tempCont==1:
                        temp4a=[]
                        temp4a.append(f1+"-"+cantidad)
                        temp4.insert(0,temp4a)
                    if tempCont==2:
                        temp4b=[]
                        temp4b.append(f1+"-"+cantidad)
                        temp4.insert(1,temp4b)
                    if tempCont==3:
                        temp4c=[]
                        temp4c.append(f1+"-"+cantidad)
                        temp4.insert(2,temp4c)
                    if tempCont==4:
                        temp4d=[]
                        temp4d.append(f1+"-"+cantidad)
                        temp4.insert(3,temp4d)
                    tempCont+=1
            if len(temp1)!=0:
                fechaS.insert(contadorS,temp1)
            if len(temp2)!=0:
                fechaS.insert(contadorS,temp2)
            if len(temp3)!=0:
                fechaS.insert(contadorS,temp3)
            if len(temp4)!=0:
                fechaS.insert(contadorS,temp4)
            contadorS+=1
        
        contTemp = 0
        for i in range(len(fechaS)):
            cantidadObjeto = []
            contS1 = 0
            contS2 = 0
            contS3 = 0
            contS4 = 0
            for j in range(len(fechaS[i])):
                temp = fechaS[i][j]
                fecha1 = temp[0].split("-")
                cantidad1 = fecha1[3]
                cantFinal = int(cantidad1)
                fecha = int(fecha1[0])
                if fecha<8:
                    contS1+=cantFinal
                if fecha>7 and fecha<15:
                    contS2+=cantFinal
                if fecha>14 and fecha<22:
                    contS3+=cantFinal
                if fecha>21 and fecha<32:
                    contS4+=cantFinal
            finalCont = contS1 + contS2 + contS3 + contS4
            cantidadObjeto.append(contS1)
            cantidadObjeto.append(contS2)
            cantidadObjeto.append(contS3)
            cantidadObjeto.append(contS4)
            cantidadObjeto.append(finalCont)
            cantidadS.insert(contTemp,cantidadObjeto)
            contTemp+=1

        fSalida.append(subcategoriasS)
        fSalida.append(cantidadS)

        return Response(self.custom_response_get(fSalida))

class reporteIndicadorBNC(APIView):
    def custom_response_get(self, response):
        res= json.dumps(response)
        response = json.loads(res)

        listResponse = []

        for i in range(len(response[0])):
            finalData={
                "Salida": response[0][i],
                "Semana1" : response[1][i][0],
                "Semana2" : response[1][i][1],
                "Semana3" : response[1][i][2],
                "Semana4" : response[1][i][3],
                "Total" : response[1][i][4],
            }
            listResponse.append(finalData)

        return listResponse

    def get(self, request, format=None):
        indicador = indicadorModel.objects.all()
        serizalicerIndicador = indicadorSerializer(indicador , many=True, context={'request':request})
        res= json.dumps(serizalicerIndicador.data)
        response = json.loads(res)

        fSalida = []            # Resultado final
        subcategoriasS = []     # Tipo CPC (Cuenta por Cobrar) - CPP (Cuentas por Pagar) - BNC (Bancos)
        fechaS = []             # Fechas en base a la posición de subcategorias
        cantidadS = []          # Cantidad

        for i in response:

            if i['tipo']=="BNC":

                # catS = i['categoria']
                # categoria = categoryModel.objects.filter(id=catS).values()
                subcategoriaRes = i['razon']
                if subcategoriaRes in subcategoriasS:
                    xample = 1
                else:
                    subcategoriasS.append(subcategoriaRes)
        
        contadorS = 0
        tamanio = len(subcategoriasS)
        
        for i in range(tamanio):
            # categoria = categoryModel.objects.filter(subcategoria=subcategoriasS[contadorS]).values()
            # flujo = flujoModel.objects.filter(categoria=categoria[0]['id']).values()
            indicador = indicadorModel.objects.filter(Q(tipo="BNC") & Q(razon=subcategoriasS[contadorS])).values()
            n = len(indicador)
            temp1 = []
            temp2 = []
            temp3 = []
            temp4 = []
            tempCont = 1
            for j in range(n):
                f1 = indicador[j]['fecha']
                cantida = indicador[j]['cantidad']
                cantidad = str(cantida)
                if n==1:
                    if tempCont==1:
                        temp1a=[]
                        temp1a.append(f1+"-"+cantidad)
                        temp1.insert(0,temp1a)
                if n==2:
                    if tempCont==1:
                        temp2a=[]
                        temp2a.append(f1+"-"+cantidad)
                        temp2.insert(0,temp2a)
                    if tempCont==2:
                        temp2b=[]
                        temp2b.append(f1+"-"+cantidad)
                        temp2.insert(1,temp2b)
                    tempCont+=1
                if n==3:
                    if tempCont==1:
                        temp3a=[]
                        temp3a.append(f1+"-"+cantidad)
                        temp3.insert(0,temp3a)
                    if tempCont==2:
                        temp3b=[]
                        temp3b.append(f1+"-"+cantidad)
                        temp3.insert(1,temp3b)
                    if tempCont==3:
                        temp3c=[]
                        temp3c.append(f1+"-"+cantidad)
                        temp3.insert(2,temp3c)
                    tempCont+=1
                if n==4:
                    if tempCont==1:
                        temp4a=[]
                        temp4a.append(f1+"-"+cantidad)
                        temp4.insert(0,temp4a)
                    if tempCont==2:
                        temp4b=[]
                        temp4b.append(f1+"-"+cantidad)
                        temp4.insert(1,temp4b)
                    if tempCont==3:
                        temp4c=[]
                        temp4c.append(f1+"-"+cantidad)
                        temp4.insert(2,temp4c)
                    if tempCont==4:
                        temp4d=[]
                        temp4d.append(f1+"-"+cantidad)
                        temp4.insert(3,temp4d)
                    tempCont+=1
            if len(temp1)!=0:
                fechaS.insert(contadorS,temp1)
            if len(temp2)!=0:
                fechaS.insert(contadorS,temp2)
            if len(temp3)!=0:
                fechaS.insert(contadorS,temp3)
            if len(temp4)!=0:
                fechaS.insert(contadorS,temp4)
            contadorS+=1
        
        contTemp = 0
        for i in range(len(fechaS)):
            cantidadObjeto = []
            contS1 = 0
            contS2 = 0
            contS3 = 0
            contS4 = 0
            for j in range(len(fechaS[i])):
                temp = fechaS[i][j]
                fecha1 = temp[0].split("-")
                cantidad1 = fecha1[3]
                cantFinal = int(cantidad1)
                fecha = int(fecha1[0])
                if fecha<8:
                    contS1+=cantFinal
                if fecha>7 and fecha<15:
                    contS2+=cantFinal
                if fecha>14 and fecha<22:
                    contS3+=cantFinal
                if fecha>21 and fecha<32:
                    contS4+=cantFinal
            finalCont = contS1 + contS2 + contS3 + contS4
            cantidadObjeto.append(contS1)
            cantidadObjeto.append(contS2)
            cantidadObjeto.append(contS3)
            cantidadObjeto.append(contS4)
            cantidadObjeto.append(finalCont)
            cantidadS.insert(contTemp,cantidadObjeto)
            contTemp+=1

        fSalida.append(subcategoriasS)
        fSalida.append(cantidadS)

        return Response(self.custom_response_get(fSalida))
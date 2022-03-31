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
            finalData = {
                "Salida": response[0][i],
                "Semana1": response[i+1][0],
                "Semana2": response[i+1][1],
                "Semana3": response[i+1][2],
                "Semana4": response[i+1][3],
                "Total": response[i+1][0] + response[i+1][1] + response[i+1][2] + response[i+1][3]
            }
            listResponse.append(finalData)
        finalData2 = {
            "Salida": "Total:",
            "Semana1" : response[3][0],
            "Semana2" : response[3][1],
            "Semana3" : response[3][2],
            "Semana4" : response[3][3],
            "Total": response[3][0] + response[3][1] + response[3][2] + response[3][3]
        }
        listResponse.append(finalData2)

        # for i in range(len(response[0])):
        #     finalData={
        #         "Salida": response[0][i],
        #         "Semana1" : response[1][i][0],
        #         "Semana2" : response[1][i][1],
        #         "Semana3" : response[1][i][2],
        #         "Semana4" : response[1][i][3],
        #         "Total" : response[1][i][4],
        #     }
        #     listResponse.append(finalData)

        # finalData2 = {
        #     "Salida": "Total:",
        #     "Semana1" : response[2],
        #     "Semana2" : response[3],
        #     "Semana3" : response[4],
        #     "Semana4" : response[5],
        #     "Total" : response[6]
        # }
        # listResponse.append(finalData2)

        return listResponse

    def get(self, request, pk, format=None):
        mes = "/"+pk+"/"
        # flujo = flujoModel.objects.all()
        flujo2 = flujoModel.objects.filter(fecha__icontains=mes)
        serializerFlujo = flujoSerializer(flujo2 , many=True, context={'request':request})
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
            flujo = flujoModel.objects.filter(Q(categoria=categoria[0]['id']) & Q(fecha__icontains=mes)).values()
            n = len(flujo)
            temp = []
            tempCont = 0
            for j in range(n):
                f1 = flujo[j]['fecha']
                cantida = flujo[j]['cantidad']
                cantidad = str(cantida)

                tempArray = []
                tempArray.append(f1+"/"+cantidad)
                temp.insert(tempCont, tempArray)
                tempCont+=1

            # if len(temp)==0:
            fechaS.insert(contadorS,temp)
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
                fecha1 = temp[0].split("/")
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

        sumaTotal=0
        sumaSem1=0
        sumaSem2=0
        sumaSem3=0
        sumaSem4=0
        for i in cantidadS:
            sumaSem1+=i[0]
            sumaSem2+=i[1]
            sumaSem3+=i[2]
            sumaSem4+=i[3]
            sumaTotal+=i[4]

        fSalida.append(subcategoriasS)
        fSalida.append(cantidadS)
        fSalida.append(sumaSem1)
        fSalida.append(sumaSem2)
        fSalida.append(sumaSem3)
        fSalida.append(sumaSem4)

        finalRes = []
        categoriaRes = []
        contSumaSemana1 = 0
        contSumaSemana2 = 0
        contSumaSemana3 = 0
        contSumaSemana4 = 0

        contSumaSemana11 = 0
        contSumaSemana21 = 0
        contSumaSemana31 = 0
        contSumaSemana41 = 0
        contSumaSemana12 = 0
        contSumaSemana22 = 0
        contSumaSemana32 = 0
        contSumaSemana42 = 0
        sumas = []
        sumas2 = []
        sumas3 = []

        tamanioSub = len(fSalida[0])
        for i in range(tamanioSub):
            categoria = categoryModel.objects.filter(subcategoria = fSalida[0][i]).values()
            catTemp = categoria[0]['categoria']
            if catTemp=="Costo-Venta":
                contSumaSemana1+=fSalida[1][i][0]
                contSumaSemana2+=fSalida[1][i][1]
                contSumaSemana3+=fSalida[1][i][2]
                contSumaSemana4+=fSalida[1][i][3]
                contSumaSemana11+=fSalida[1][i][0]
                contSumaSemana21+=fSalida[1][i][1]
                contSumaSemana31+=fSalida[1][i][2]
                contSumaSemana41+=fSalida[1][i][3]
                if catTemp in categoriaRes:
                    example = 1
                else:
                    categoriaRes.append(catTemp)
            if catTemp=="Gasto-AOC":
                contSumaSemana1+=fSalida[1][i][0]
                contSumaSemana2+=fSalida[1][i][1]
                contSumaSemana3+=fSalida[1][i][2]
                contSumaSemana4+=fSalida[1][i][3]
                contSumaSemana12+=fSalida[1][i][0]
                contSumaSemana22+=fSalida[1][i][1]
                contSumaSemana32+=fSalida[1][i][2]
                contSumaSemana42+=fSalida[1][i][3]
                if catTemp in categoriaRes:
                    example = 1
                else:
                    categoriaRes.append(catTemp)
            
        sumas.append(contSumaSemana1)
        sumas.append(contSumaSemana2)
        sumas.append(contSumaSemana3)
        sumas.append(contSumaSemana4)
        sumas2.append(contSumaSemana11)
        sumas2.append(contSumaSemana21)
        sumas2.append(contSumaSemana31)
        sumas2.append(contSumaSemana41)
        sumas3.append(contSumaSemana12)
        sumas3.append(contSumaSemana22)
        sumas3.append(contSumaSemana32)
        sumas3.append(contSumaSemana42)

        finalRes.append(categoriaRes)
        finalRes.append(sumas2)
        finalRes.append(sumas3)
        finalRes.append(sumas)
        print(finalRes)
        
        fSalida.append(sumaTotal)

        return Response(self.custom_response_get(finalRes))

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

        finalData2 = {
            "Salida": "Total:",
            "Semana1" : response[2],
            "Semana2" : response[3],
            "Semana3" : response[4],
            "Semana4" : response[5],
            "Total" : response[6]
        }
        listResponse.append(finalData2)


        return listResponse

    def get(self, request, pk, format=None):
        mes = "/"+pk+"/"
        # flujo = flujoModel.objects.all()
        flujo2 = flujoModel.objects.filter(fecha__icontains=mes)
        serializerFlujo = flujoSerializer(flujo2 , many=True, context={'request':request})
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
            flujo = flujoModel.objects.filter(Q(categoria=categoria[0]['id']) & Q(fecha__icontains=mes)).values()
            n = len(flujo)
            temp = []
            tempCont = 0
            for j in range(n):
                f1 = flujo[j]['fecha']
                cantida = flujo[j]['cantidad']
                cantidad = str(cantida)

                tempArray = []
                tempArray.append(f1+"/"+cantidad)
                temp.insert(tempCont, tempArray)
                tempCont+=1

            # if len(temp)==0:
            fechaS.insert(contadorS,temp)
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
                fecha1 = temp[0].split("/")
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

        sumaTotal=0
        sumaSem1=0
        sumaSem2=0
        sumaSem3=0
        sumaSem4=0
        for i in cantidadS:
            sumaSem1+=i[0]
            sumaSem2+=i[1]
            sumaSem3+=i[2]
            sumaSem4+=i[3]
            sumaTotal+=i[4]

        fSalida.append(subcategoriasS)
        fSalida.append(cantidadS)
        fSalida.append(sumaSem1)
        fSalida.append(sumaSem2)
        fSalida.append(sumaSem3)
        fSalida.append(sumaSem4)
        fSalida.append(sumaTotal)

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

        finalData2 = {
            "Salida": "Total:",
            "Semana1" : response[2],
            "Semana2" : response[3],
            "Semana3" : response[4],
            "Semana4" : response[5],
            "Total" : response[6]
        }
        listResponse.append(finalData2)


        return listResponse

    def get(self, request, pk, format=None):
        mes = "/"+pk+"/"
        indicador = indicadorModel.objects.filter(fecha__icontains=mes)
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
            indicador = indicadorModel.objects.filter(Q(tipo="CPC") & Q(razon=subcategoriasS[contadorS]) & Q(fecha__icontains=mes)).values()
            n = len(indicador)
            temp = []
            tempCont = 0
            for j in range(n):
                f1 = indicador[j]['fecha']
                cantida = indicador[j]['cantidad']
                cantidad = str(cantida)

                tempArray = []
                tempArray.append(f1+"/"+cantidad)
                temp.insert(tempCont, tempArray)
                tempCont+=1

            # if len(temp)==0:
            fechaS.insert(contadorS,temp)
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
                fecha1 = temp[0].split("/")
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

        sumaTotal=0
        sumaSem1=0
        sumaSem2=0
        sumaSem3=0
        sumaSem4=0
        for i in cantidadS:
            sumaSem1+=i[0]
            sumaSem2+=i[1]
            sumaSem3+=i[2]
            sumaSem4+=i[3]
            sumaTotal+=i[4]

        fSalida.append(subcategoriasS)
        fSalida.append(cantidadS)
        fSalida.append(sumaSem1)
        fSalida.append(sumaSem2)
        fSalida.append(sumaSem3)
        fSalida.append(sumaSem4)
        fSalida.append(sumaTotal)

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

        finalData2 = {
            "Salida": "Total:",
            "Semana1" : response[2],
            "Semana2" : response[3],
            "Semana3" : response[4],
            "Semana4" : response[5],
            "Total" : response[6]
        }
        listResponse.append(finalData2)


        return listResponse

    def get(self, request, pk, format=None):
        mes = "/"+pk+"/"
        indicador = indicadorModel.objects.filter(fecha__icontains=mes)
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
            indicador = indicadorModel.objects.filter(Q(tipo="CPP") & Q(razon=subcategoriasS[contadorS]) & Q(fecha__icontains=mes)).values()
            n = len(indicador)
            temp = []
            tempCont = 0
            for j in range(n):
                f1 = indicador[j]['fecha']
                cantida = indicador[j]['cantidad']
                cantidad = str(cantida)

                tempArray = []
                tempArray.append(f1+"/"+cantidad)
                temp.insert(tempCont, tempArray)
                tempCont+=1

            # if len(temp)==0:
            fechaS.insert(contadorS,temp)
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
                fecha1 = temp[0].split("/")
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

        sumaTotal=0
        sumaSem1=0
        sumaSem2=0
        sumaSem3=0
        sumaSem4=0
        for i in cantidadS:
            sumaSem1+=i[0]
            sumaSem2+=i[1]
            sumaSem3+=i[2]
            sumaSem4+=i[3]
            sumaTotal+=i[4]

        fSalida.append(subcategoriasS)
        fSalida.append(cantidadS)
        fSalida.append(sumaSem1)
        fSalida.append(sumaSem2)
        fSalida.append(sumaSem3)
        fSalida.append(sumaSem4)
        fSalida.append(sumaTotal)

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

        finalData2 = {
            "Salida": "Total:",
            "Semana1" : response[2],
            "Semana2" : response[3],
            "Semana3" : response[4],
            "Semana4" : response[5],
            "Total" : response[6]
        }
        listResponse.append(finalData2)


        return listResponse

    def get(self, request, pk, format=None):
        mes = "/"+pk+"/"
        indicador = indicadorModel.objects.filter(fecha__icontains=mes)
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
            indicador = indicadorModel.objects.filter(Q(tipo="BNC") & Q(razon=subcategoriasS[contadorS]) & Q(fecha__icontains=mes)).values()
            n = len(indicador)
            temp = []
            tempCont = 0
            for j in range(n):
                f1 = indicador[j]['fecha']
                cantida = indicador[j]['cantidad']
                cantidad = str(cantida)

                tempArray = []
                tempArray.append(f1+"/"+cantidad)
                temp.insert(tempCont, tempArray)
                tempCont+=1

            # if len(temp)==0:
            fechaS.insert(contadorS,temp)
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
                fecha1 = temp[0].split("/")
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

        sumaTotal=0
        sumaSem1=0
        sumaSem2=0
        sumaSem3=0
        sumaSem4=0
        for i in cantidadS:
            sumaSem1+=i[0]
            sumaSem2+=i[1]
            sumaSem3+=i[2]
            sumaSem4+=i[3]
            sumaTotal+=i[4]

        fSalida.append(subcategoriasS)
        fSalida.append(cantidadS)
        fSalida.append(sumaSem1)
        fSalida.append(sumaSem2)
        fSalida.append(sumaSem3)
        fSalida.append(sumaSem4)
        fSalida.append(sumaTotal)

        return Response(self.custom_response_get(fSalida))
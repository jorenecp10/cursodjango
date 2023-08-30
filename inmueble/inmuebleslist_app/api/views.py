from inmuebleslist_app.models import Edificacion,Empresa
from inmuebleslist_app.api.serializers import EdificacionSerializer,EmpresaSerializer
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView


class EmpresaAV(APIView):
    
    def get(self,request):
        empresa= Empresa.objects.all()
        serializer = EmpresaSerializer(empresa,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = EmpresaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)    
        
        

class EdificacionAV(APIView):
    
    def get(self,request):
        edificacion= Edificacion.objects.all()
        serializer = EdificacionSerializer(edificacion,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer=EdificacionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class EdificacionDetalleAV(APIView):
    
    def get(self,request,pk):
        try:
            edificacion = Edificacion.objects.get(pk=pk)
        except Edificacion.DoesNotExist:
            return Response({'error':'Inmueble no encontrado'},status=status.HTTP_404_NOT_FOUND)
        
        serializer=EdificacionSerializer(edificacion)
        return Response(serializer.data)
    
    def put(self,request,pk):
        try:
            edificacion = Edificacion.objects.get(pk=pk)
        except Edificacion.DoesNotExist:
            return Response({'error':'Inmueble no encontrado'},status=status.HTTP_404_NOT_FOUND)
        
        serializer=EdificacionSerializer(edificacion,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):    
        try:
            edificacion = EdificacionSerializer.objects.get(pk=pk)
        except Edificacion.DoesNotExist:
            return Response({'error':'Inmueble no encontrado'},status=status.HTTP_404_NOT_FOUND)
        
        edificacion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
       
        
        
        
    
    
        

# @api_view(['GET','POST'])

# def inmueble_list(request):
#     if request.method == 'GET':
#         inmuebles = Inmueble.objects.all()
#         serializer = InmuebleSerializer(inmuebles, many=True)
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         de_seriallizar=InmuebleSerializer(data=request.data)
#         if de_seriallizar.is_valid():
#             de_seriallizar.save()
#             return Response(de_seriallizar.data)
#         else:
#             return Response(de_seriallizar.errors)
            
# @api_view(['GET','PUT','DELETE'])   
# def inmueble_detalle(request,pk):
#     if request.method == 'GET':
#         try:    
#             inmueble = Inmueble.objects.get(pk=pk)
#             serializer = InmuebleSerializer(inmueble)
#             return Response(serializer.data)
#         except Inmueble.DoesNotExist:
#             return Response('Error: el inmueble no existe',status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'PUT':
#         inmueble = Inmueble.objects.get(pk=pk)
#         de_seriallizar=InmuebleSerializer(inmueble,data=request.data)
       
#         if de_seriallizar.is_valid():
#            de_seriallizar.save()
#            return Response(de_seriallizar.data)
#         else:
#             return Response(de_seriallizar.errors,status=status.HTTP_400_BAD_REQUEST)
    
#     if request.method == 'DELETE':
#         try:
#             inmueble = Inmueble.objects.get(pk=pk)
#             inmueble.delete()
#         except Inmueble.DoesNotExist:
#             return Response('Error: el inmueble no existe',status=status.HTTP_404_NOT_FOUND)    
#         return Response(status.HTTP_204_NO_CONTENT)
    


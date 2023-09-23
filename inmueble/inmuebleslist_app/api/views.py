from inmuebleslist_app.models import Edificacion,Empresa,Comentario
from inmuebleslist_app.api.serializers import EdificacionSerializer,EmpresaSerializer,ComentarioSerializer
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import  generics,mixins
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from inmuebleslist_app.api.permissions import AdminOrReadOnly,ComentarioUserOrReadOnly

class ComentarioCreate(generics.CreateAPIView):
    serializer_class = ComentarioSerializer
    def get_queryset(self):
        return Comentario.objects.all()
    
    def perform_create(self,serializer):
        pk = self.kwargs.get('pk')
        inmueble= Edificacion.objects.get(pk=pk)
        user = self.request.user
        comentario_queryset = Comentario.objects.filter(edificacion=inmueble,comentario_user=user)
        if comentario_queryset.exists():
            raise ValidationError("El usuario ya escribio un comentario para este inmueble")
        
        if inmueble.number_calificacion == 0:
            inmueble.avg_calificacion = 5
        else:
            inmueble.avg_calificacion = (serializer.validated_data['calificacion'] + inmueble.avg_calificacion)/2
            
        inmueble.number_calificacion = inmueble.number_calificacion + 1
        inmueble.save()
        serializer.save(edificacion=inmueble,comentario_user=user)
        

class ComentarioList(generics.ListCreateAPIView):
    # queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Comentario.objects.filter(edificacion=pk)
    

        
class ComentarioDetail(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    permission_classes = [ComentarioUserOrReadOnly]
    
    

# class ComentarioList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = Comentario.objects.all()
#     serializer_class = ComentarioSerializer

#     def get(self,request, *args, **kwargs):
#         return self.list(request,*args, **kwargs)

#     def post(self,request, *args,**kwargs):
#         return self.create(request,*args,**kwargs)

# class ComentarioDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
#     queryset = Comentario.objects.all()
#     serializer_class = ComentarioSerializer

#     def get(self,request, *args, **kwargs):
#         return self.retrieve(request,*args, **kwargs)

    # def put(self,request, *args, **kwargs):
    #     return self.update(request,*args, **kwargs)

class EmpresaVS(viewsets.ModelViewSet):
    permission_classes = [AdminOrReadOnly]
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

# class EmpresaVS(viewsets.ViewSet):
    
#     def list(self,request):
#         queryset= Empresa.objects.all()
#         serializer = EmpresaSerializer(queryset,many=True)
#         return Response(serializer.data)
    
#     def retrieve(self, request, pk=None):
#         queryset=Empresa.objects.all()
#         edificacionlist = get_object_or_404(queryset,pk=pk)
#         serializer=EmpresaSerializer(edificacionlist)
#         return Response(serializer.data)
    
#     def create(self,request):
#         serializer = EmpresaSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
#     def update(self,request,pk):
#         try:
#             empresa = Empresa.objects.get(pk=pk)
#         except Empresa.DoesNotExist:
#             return Response({'error':'Empresa no encontrado'},status=status.HTTP_404_NOT_FOUND)
#         serializer=EmpresaSerializer(empresa,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)    
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
#     def destroy(self,request,pk):
#         try:
#             empresa = Empresa.objects.get(pk=pk)
#         except Empresa.DoesNotExist:
#             return Response({'error':'Empresa no encontrado'},status=status.HTTP_404_NOT_FOUND)
#         empresa.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
        
        
        
    
        
        
        

class EmpresaAV(APIView):

    def get(self,request):
        empresa= Empresa.objects.all()
        serializer = EmpresaSerializer(empresa,many=True,context={'request':request})
        return Response(serializer.data)

    def post(self,request):
        serializer = EmpresaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


class EmpresaDetalleAV(APIView):
    def get(self,request,pk):
        try:
            empresa = Empresa.objects.get(pk=pk)
        except Empresa.DoesNotExist:
            return Response({'error':'Empresa no encontrado'},status=status.HTTP_404_NOT_FOUND)

        serializer = EmpresaSerializer(empresa,context={'request':request})
        return Response(serializer.data)

    def put(self,request,pk):
        try:
            empresa = Empresa.objects.get(pk=pk)
        except Empresa.DoesNotExist:
            return Response({'error':'Empresa no encontrado'},status=status.HTTP_404_NOT_FOUND)

        serializer=EmpresaSerializer(empresa,data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        try:
            empresa = Empresa.objects.get(pk=pk)
        except Empresa.DoesNotExist:
            return Response({'error':'Empresa no encontrado'},status=status.HTTP_404_NOT_FOUND)

        empresa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)









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



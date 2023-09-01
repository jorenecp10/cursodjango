from django.contrib import admin

# Register your models here.
from inmuebleslist_app.models import Edificacion,Empresa,Comentario

admin.site.register(Edificacion)         
admin.site.register(Empresa) 
admin.site.register(Comentario)     

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[

path('', views.hello),
 
path('contacto/', views.guardar_contacto, name='guardar_contacto'),
    # URL alternativa si usas la vista con formularios de Django
path('contacto-form/', views.contacto_form_view, name='contacto_form'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

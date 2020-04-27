from django.urls import path
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
# path('', views.index, name='index'),
path('', password, name='password'),
path('sense/', sense, name='sense'),
path('home/', home, name='homepage'),
#path('info/', sense, name='ingredient_information'),
path('info/',sense , name='info'),
path('safe/',sense , name='safe'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

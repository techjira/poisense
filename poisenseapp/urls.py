from django.urls import path
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include

urlpatterns = [
# path('', views.index, name='index'),
path('header', header, name='header'),
path('footer', footer, name='footer'),
path('', password, name='password'),
path('sense/', sense, name='sense'),
path('home/', home, name='homepage'),
path('allergy-detection/', allergy, name='allergy-detection'),
path('info/',sense , name='info'),
path('allergy-info/', allergy, name='allergy-info'),
# path('.well-known/acme-challenge/YWObyQs8K90gboL2UYaiKB6_k2emxhUuG-mZQ7yOg4c',ssl , name='.well-known/acme-challenge/YWObyQs8K90gboL2UYaiKB6_k2emxhUuG-mZQ7yOg4c'),
# path('.well-known/acme-challenge/51_a9PO7gke53ZMZV0kbWLwiLIAn9xM2gsPFEaQS2j0',ssl2 , name='.well-known/acme-challenge/51_a9PO7gke53ZMZV0kbWLwiLIAn9xM2gsPFEaQS2j0'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

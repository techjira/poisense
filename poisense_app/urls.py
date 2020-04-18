from django.conf.urls import url
from poisense_app import views

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url('',views.help,name='help'),

]

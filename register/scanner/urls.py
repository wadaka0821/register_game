from django.urls import path

from . import views

app_name = 'scanner'

urlpatterns = [
    path('', views.index, name='index'),
    path('<uuid:history_id>/', views.purchase, name='purchase'),
    path('count_up/', views.count_up, name='count_up')
]
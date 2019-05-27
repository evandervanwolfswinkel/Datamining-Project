from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Diseases/', views.circle_diseases, name='circle_diseases'),
    path('Compounds/', views.circle_compounds, name='circle_compounds')
]
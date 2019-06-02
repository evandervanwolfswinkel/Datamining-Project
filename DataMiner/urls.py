from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Diseases/', views.circle_diseases, name='circle_diseases'),
    path('Compounds/', views.circle_compounds, name='circle_compounds'),
    path('Database/', views.database, name='database'),
    path('UpdatingRelationships/', views.update_relationships, name='update_relationships'),
    path('About/', views.about, name='about')

]
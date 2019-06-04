from django.urls import path
from django.conf.urls.static import static
from django.contrib.staticfiles.views import serve
from django.views.decorators.cache import cache_control
from Datamining_Project import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Diseases/', views.circle_diseases, name='circle_diseases'),
    path('Compounds/', views.circle_compounds, name='circle_compounds'),
    path('Database/', views.database, name='database'),
    path('UpdatingRelationships/', views.update_relationships, name='update_relationships'),
    path('UpdatingDatabase/', views.update_database, name='update_database'),
    path('Error/', views.error, name='error'),
    path('About/', views.about, name='about')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, view=cache_control(no_cache=True, must_revalidate=True)(serve))
if settings.DEBUG == False:
    urlpatterns += static(settings.STATIC_URL, view=cache_control(no_cache=True, must_revalidate=True)(serve))
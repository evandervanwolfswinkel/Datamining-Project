from django.shortcuts import render
import VisualisationLogic
# Create your views here.
def index(request):
    return render(request, "index.html")

def circle_diseases(request):
    return render(request, "circle_diseases.html")

def circle_compounds(request):
    return render(request, "circle_compounds.html")
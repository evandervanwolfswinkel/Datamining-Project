from django.shortcuts import render
import VisualisationLogic
from DbInteractions import DbInteractions

# Create your views here.
def index(request):
    return render(request, "index.html")

def circle_diseases(request):
    return render(request, "circle_diseases.html")

def circle_compounds(request):
    return render(request, "circle_compounds.html")

def database(request):
    dbi = DbInteractions()
    term_lists = dbi.get_lists()
    bitter_snym_list = term_lists[0]
    disease_snym_list = term_lists[1]
    compound_snym_list = term_lists[2]

    return render(request, "database.html", {'disease_list':disease_snym_list,
                                             'compound_list':compound_snym_list,
                                             'bitter_list':bitter_snym_list})
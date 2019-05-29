from django.shortcuts import render, HttpResponseRedirect
from VisualisationLogic import set_value, write_json
from DbInteractions import DbInteractions

# Create your views here.
def index(request):
    return render(request, "index.html")

def circle_diseases(request):
    dbi = DbInteractions()
    dict_dis = dbi.get_relations()[0]
    dict_dis = set_value(dict_dis)
    write_json(dict_dis, "diseases")
    term_lists = dbi.get_lists()
    compound_snym_list = term_lists[2]
    return render(request, "circle_diseases.html", {'compound_list':compound_snym_list})

def circle_compounds(request):
    dbi = DbInteractions()
    dict_dis = dbi.get_relations()[1]
    dict_dis = set_value(dict_dis)
    write_json(dict_dis, "compounds")
    term_lists = dbi.get_lists()
    disease_snym_list = term_lists[1]
    return render(request, "circle_compounds.html", {'disease_list':disease_snym_list})

def database(request):
    dbi = DbInteractions()
    if request.method == 'GET':
        type = request.GET.get('type')
        function = request.GET.get('function')
        term = request.GET.get('term')
        if type == 'dis':
            if function == 'add':
                dbi.add_rm('dis', term, True)
                return HttpResponseRedirect('/DataMiner/Database/')
            if function == 'remove':
                dbi.add_rm('dis', term, False)
                return HttpResponseRedirect('/DataMiner/Database/')
        if type == 'comp':
            if function == 'add':
                dbi.add_rm('comp', term, True)
                return HttpResponseRedirect('/DataMiner/Database/')
            if function == 'remove':
                dbi.add_rm('comp', term, False)
                return HttpResponseRedirect('/DataMiner/Database/')

    term_lists = dbi.get_lists()
    bitter_snym_list = term_lists[0]
    disease_snym_list = term_lists[1]
    compound_snym_list = term_lists[2]
    relationcount = dbi.get_relation_amount()
    articlecount = dbi.get_db_length()
    return render(request, "database.html", {'disease_list':disease_snym_list,
                                             'compound_list':compound_snym_list,
                                             'bitter_list':bitter_snym_list,
                                             'relationcount': relationcount,
                                             'articlecount': articlecount})

def update_relationships(request):
    dbi = DbInteractions()
    if request.method == 'POST':
        dbi.update_relations()
        return HttpResponseRedirect('/DataMiner/Database/')
    else:
        return HttpResponseRedirect('/DataMiner/Database/')
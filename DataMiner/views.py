from django.shortcuts import render, HttpResponseRedirect
from VisualisationLogic import set_value, write_circlejson, writetofile, openjson
from DbInteractions import DbInteractions


def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def circle_diseases(request):
    compound_snym_list = openjson("compoundtermlist")
    articlejson = openjson("articlesdis")
    return render(request, "circle_diseases.html", {'compound_list':compound_snym_list,'articledislist':articlejson})

def circle_compounds(request):
    disease_snym_list = openjson("diseasetermlist")
    articlejson = openjson("articlescomp")
    return render(request, "circle_compounds.html", {'disease_list':disease_snym_list,'articlecomplist':articlejson})

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
        term_lists = dbi.get_lists()
        write_circlejson(set_value(dbi.get_relations()[0]), "diseases")
        write_circlejson(set_value(dbi.get_relations()[1]), "compounds")
        writetofile(dbi.return_json_termlist(term_lists[1]), "diseasetermlist")
        writetofile(dbi.return_json_termlist(term_lists[2]), "compoundtermlist")
        writetofile(dbi.return_article_dict(dbi.get_relations()[0]), "articlesdis")
        writetofile(dbi.return_article_dict(dbi.get_relations()[1]), "articlescomp")
        return HttpResponseRedirect('/DataMiner/Database/')
    else:
        return HttpResponseRedirect('/DataMiner/Database/')
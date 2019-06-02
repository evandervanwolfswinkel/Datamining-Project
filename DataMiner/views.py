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
        if type == 'bg':
            if function == 'add':
                dbi.add_rm('bg', term, True)
                return HttpResponseRedirect('/DataMiner/Database/')
            if function == 'remove':
                dbi.add_rm('bg', term, False)
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
        disease_term_list = term_lists[1]
        compound_term_list = term_lists[2]
        disease_relations = dbi.get_relations()[0]
        compound_relations = dbi.get_relations()[1]
        article_disease_dict = dbi.return_article_dict(disease_relations)
        article_compound_dict = dbi.return_article_dict(compound_relations)
        value_disease_relations = set_value(disease_relations)
        value_compound_relations = set_value(compound_relations)
        write_circlejson(value_disease_relations, "diseases")
        write_circlejson(value_compound_relations, "compounds")
        writetofile(dbi.return_json_termlist(disease_term_list), "diseasetermlist")
        writetofile(dbi.return_json_termlist(compound_term_list), "compoundtermlist")
        writetofile(article_disease_dict, "articlesdis")
        writetofile(article_compound_dict, "articlescomp")
        return HttpResponseRedirect('/DataMiner/Database/')
    else:
        return HttpResponseRedirect('/DataMiner/Database/')

def update_database(request):
    dbi = DbInteractions()
    if request.method == 'POST':
        dbi.renew_db()
        return HttpResponseRedirect('/DataMiner/Database/')
    else:
        return HttpResponseRedirect('/DataMiner/Database/')
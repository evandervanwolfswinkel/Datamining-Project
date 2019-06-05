from django.shortcuts import render, HttpResponseRedirect
from VisualisationLogic import set_value, write_circlejson, writetofile, openjson
from DbInteractions import DbInteractions
"""
@:Author: Evander van Wolfswinkel
@:Date last edited: 4-6-2019
@:Function: Below functions are used as views that are connected to URLS in urls.py
"""

def error(request):
    """
    GET requests error messages and parses them into HTML error page
    :param request:
    :return: error.html, errormessage
    """
    errormessage = request.GET.get('error')
    return render(request, "error.html", {'errormessage':errormessage})

def index(request):
    """
    Loads index page on request
    :param request:
    :return: index.html
    :except: error.html, error
    """
    try:
        return render(request, "index.html")
    except:
        error = "Index not found"
        return HttpResponseRedirect('/DataMiner/Error/?error=%s' % error)

def about(request):
    """
    Loads about page on request
    :param request:
    :return: about.html
    :except: error.html, error
    """
    try:
        return render(request, "about.html")
    except:
        error = "About page not found"
        return HttpResponseRedirect('/DataMiner/Error/?error=%s'%error)


def circle_diseases(request):
    """
    Loads circle packing disease json visualisation, and corresponding article and term list
    :param request:
    :return: circle_disease.html, compound_snym_list, articlejson
    :except try openjson:
    :returns: error.html, errormessage
    :except try load page:
    :returns: error.html, errormessage
    """
    try:
        compound_snym_list = openjson("compoundtermlist")
        articlejson = openjson("articlesdis")
    except:
        error = 'articles and termlist could not be loaded'
        HttpResponseRedirect('/DataMiner/Error/?error=%s'%error)
    try:
        return render(request, "circle_diseases.html", {'compound_list':compound_snym_list,
                                                    'articledislist':articlejson})
    except:
        error = "Disease page not found"
        return HttpResponseRedirect('/DataMiner/Error/?error=%s' % error)

def circle_compounds(request):
    """
    Loads circle packing compound json visualisation, and corresponding article and term list
    :param request:
    :return: circle_compounds.html, disease_snym_list, articlejson
    :except try openjson:
    :returns: error.html, errormessage
    :except try load page:
    :returns: error.html, errormessage
    """
    try:
        disease_snym_list = openjson("diseasetermlist")
        articlejson = openjson("articlescomp")
    except:
        error = 'articles and termlist could not be loaded'
        HttpResponseRedirect('/DataMiner/Error/?error=%s'%error)
    try:
        return render(request, "circle_compounds.html", {'disease_list':disease_snym_list,
                                                     'articlecomplist':articlejson})
    except:
        error = "Compound page not found"
        return HttpResponseRedirect('/DataMiner/Error/?error=%s' % error)

def database(request):
    """
    Loads database page with form for updating or changing database parameters
    :param request:
    :return: database.html, disease_snym_list, compound_snym_list, bitter_snym_list, relationcount, articlecount
    :except try return database.html ect:
    :returns: error.html, error
    """
    dbi = DbInteractions()
    if request.method == 'GET':
        type = request.GET.get('type')
        if type == "":
            error = "Term type not defined"
            return HttpResponseRedirect('/DataMiner/Error/?error=%s'%error)
        function = request.GET.get('function')
        if function == "":
            error = "Function type not defined"
            return HttpResponseRedirect('/DataMiner/Error/?error=%s'%error)
        term = request.GET.get('term')
        if term == "":
            error = "Term not defined"
            return HttpResponseRedirect('/DataMiner/Error/?error=%s'%error)
        if function == "add":
            dbi.add_rm(str(type), term, True)
            return HttpResponseRedirect('/DataMiner/Database/')
        if function == "remove":
            dbi.add_rm(str(type), term, False)
            return HttpResponseRedirect('/DataMiner/Database/')
    term_lists = dbi.get_lists()
    bitter_snym_list = term_lists[0]
    disease_snym_list = term_lists[1]
    compound_snym_list = term_lists[2]
    relationcount = dbi.get_relation_amount()
    articlecount = dbi.get_db_length()
    try:
        return render(request, "database.html", {'disease_list':disease_snym_list,
                                             'compound_list':compound_snym_list,
                                             'bitter_list':bitter_snym_list,
                                             'relationcount': relationcount,
                                             'articlecount': articlecount})
    except:
        error = "Database page not found"
        return HttpResponseRedirect('/DataMiner/Error/?error=%s' % error)

def update_relationships(request):
    """
    views for updating relationships on POST request, doesnt show html page
    :param request: POST
    :return: /DataMiner/Database
    :except:
    :returns: error.html, error
    """
    dbi = DbInteractions()
    if request.method == 'POST':
        try:
            dbi.update_relations()
        except:
            error = "Updating relationships went wrong, this could mean the database is offline or overloading"
            return HttpResponseRedirect('/DataMiner/Error/?error=%s' % error)
        try:
            term_lists = dbi.get_lists()
            disease_term_list = term_lists[1]
            compound_term_list = term_lists[2]
        except:
            error = "Getting new terms from database went wrong, this could mean the database is offline or overloading"
            return HttpResponseRedirect('/DataMiner/Error/?error=%s' % error)
        try:
            disease_relations = dbi.get_relations()[0]
            compound_relations = dbi.get_relations()[1]
            article_disease_dict = dbi.return_article_dict(disease_relations)
            article_compound_dict = dbi.return_article_dict(compound_relations)
            value_disease_relations = set_value(disease_relations)
            value_compound_relations = set_value(compound_relations)
        except:
            error = "Getting new relationships went wrong, this could mean the database is offline or overloading"
            return HttpResponseRedirect('/DataMiner/Error/?error=%s' % error)
        try:
            write_circlejson(value_disease_relations, "diseases")
            write_circlejson(value_compound_relations, "compounds")
            writetofile(dbi.return_json_termlist(disease_term_list), "diseasetermlist")
            writetofile(dbi.return_json_termlist(compound_term_list), "compoundtermlist")
            writetofile(article_disease_dict, "articlesdis")
            writetofile(article_compound_dict, "articlescomp")
        except:
            error = "Writing JSON files went wrong, this could be a database error or bug"
            return HttpResponseRedirect('/DataMiner/Error/?error=%s' % error)
        return HttpResponseRedirect('/DataMiner/Database/')
    else:
        return HttpResponseRedirect('/DataMiner/Database/')

def update_database(request):
    """
    Update database on POST request, doesnt load html page
    :param request: POST
    :return: /DataMiner/Database/
    :except:
    :returns: error.html, error
    """
    dbi = DbInteractions()
    if request.method == 'POST':
        dbi.renew_db()
        try:
            term_lists = dbi.get_lists()
            disease_term_list = term_lists[1]
            compound_term_list = term_lists[2]
        except:
            error = "Getting new terms from database went wrong, this could mean the database is offline or overloading"
            return HttpResponseRedirect('/DataMiner/Error/?error=%s' % error)
        try:
            disease_relations = dbi.get_relations()[0]
            compound_relations = dbi.get_relations()[1]
            article_disease_dict = dbi.return_article_dict(disease_relations)
            article_compound_dict = dbi.return_article_dict(compound_relations)
            value_disease_relations = set_value(disease_relations)
            value_compound_relations = set_value(compound_relations)
        except:
            error = "Getting new relationships went wrong, this could mean the database is offline or overloading"
            return HttpResponseRedirect('/DataMiner/Error/?error=%s' % error)
        try:
            write_circlejson(value_disease_relations, "diseases")
            write_circlejson(value_compound_relations, "compounds")
            writetofile(dbi.return_json_termlist(disease_term_list), "diseasetermlist")
            writetofile(dbi.return_json_termlist(compound_term_list), "compoundtermlist")
            writetofile(article_disease_dict, "articlesdis")
            writetofile(article_compound_dict, "articlescomp")
        except:
            error = "Writing JSON files went wrong, this could be a database error or bug"
            return HttpResponseRedirect('/DataMiner/Error/?error=%s' % error)
        return HttpResponseRedirect('/DataMiner/Database/')
    else:
        return HttpResponseRedirect('/DataMiner/Database/')
# Author: Valerie Verhalle
# Projectgroup: tutor blok 8
# date: 28-5-2019

import json


def write_circlejson(dict, name):
    """ Deze functie zet de variabele dict om naar een json file

    :param         dict, de gegenereerde dictionary in de functie: set_value  {key 1 : {key 2 : integer} }
    :param         name, een variabele die aangeeft of key 1 diseaes of compounds bevat.
    :return        als return schrijft deze functie een bestand 'compounds.json' of 'diseases.json' weg.
    """

    control_list = []
    child_dict = {}
    full_dict = {"name": "{}".format(name),
                 "children": []}
    for key1 in dict.keys():
        for key2 in dict[key1].keys():

            if key1 not in control_list:

                control_list.append(key1)
                child_dict = [{"name": key2,
                               "size": dict[key1][key2]}]

            elif key1 in control_list:

                child2_dict = {"name": key2,
                               "size": dict[key1][key2]}
                child_dict.append(child2_dict)

        full_dict["children"].append({"name": key1, "children": child_dict})

    dic_tem = json.dumps(full_dict, indent=4)
    writetofile(dic_tem, name)


def set_value(dict):
    """Deze functie telt het aantal pubmedID's per combinatie van
       termen (obesitas en kinase, obesitas en gallic acid etc)

       :param dict:     een dictionary met hierin een dictionary {key 1 : {key 2 : [pubmedID's] } }.
       :return          een dictionary met hierin een dictionary,
                        de value is nu een integer van het aantal pubmedID's {key 1 : {key 2 : integer} }
       """
    for key1 in dict.keys():
        for key2 in dict[key1].keys():
            dict[key1][key2] = len(dict[key1][key2])

    return dict


def writetofile(data, name):
    """ Deze functie schrijft de eerder gegenereerde dictionary om naar een JSON file.

    :param data:        raw data from the SQL database
    :param name:        een string die aangeeft of de param 'data' diseases of compounds als eerste key bevat
    :return:            een bestand genaamd 'diseases' of 'compounds' dat wordt weggeschreven
    """
    with open(definestaticpath() + '{}.json'.format(name), 'w') as file:
        file.write(data)
        file.close()


def openjson(name):
    """ Deze functie opent het eerder weggeschreven JSON file

    :param name:        een string die aangeeft om welk te openen file het gaat 'diseases' of 'compounds'
    :return:            het geopende bestand 'jsonobj'
    """
    path = definestaticpath()
    with open(path + '{}.json'.format(name)) as file:
        jsonobj = json.load(file)
    return jsonobj


def definestaticpath():
    """ Deze functie returnt een file paht

    :return: file path
    """
    path = "DataMiner/static/"
    return path

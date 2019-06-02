# Author: Valerie Verhalle
# Projectgroup: tutor blok 8
# date: 28-5-2019

import json

""" functie: hardgecodeerde dictionaries zoals ze uit de database opgehaald worden
return: deze functie returnt de dictionarys 'diseaes' en 'compounds'
"""


def dictionaries():
    diseases = {'cancer': {
        'kinase': [23475945, 25488547, 26537230, 21429659, 22266361, 19789297, 27748816, 22191569, 23533514, 26370527,
                   26018422, 26764240, 22272214, 26926586, 26487740, 23843889, 25264226, 15236800, 20731662, 24789581],
        'gallic acid': [17566887, 18515231], 'caffeic acid': [26370527], 'catechin': [18515231]},
        'Melanoma': {'kinase': [26537230, 26370527], 'caffeic acid': [26370527]},
        'obesity': {'kinase': [22623391, 31005847, 27751827, 27973445, 29892950, 18355726],
                    'catechin': [26778479]}}

    compounds = {'kinase': {
        'cancer': [23475945, 25488547, 26537230, 21429659, 22266361, 19789297, 27748816, 22191569, 23533514, 26370527,
                   26018422, 26764240, 22272214, 26926586, 26487740, 23843889, 25264226, 15236800, 20731662, 24789581],
        'Melanoma': [26537230, 26370527], 'obesity': [22623391, 31005847, 27751827, 27973445, 29892950, 18355726]},
        'gallic acid': {'cancer': [17566887, 18515231]},
        'caffeic acid': {'cancer': [26370527], 'Melanoma': [26370527]},
        'catechin': {'obesity': [26778479], 'cancer': [18515231]}}

    return diseases, compounds


""" functie: zet de variabele dict om naar een json file
ict: de gegenereerde dictionary in de fucntie: set_value  {key 1 : {key 2 : integer} }
name: een variabele die aangeeft of key 1 diseaes of compounds bevat.
return: als return schrijft deze functie een bestand 'compounds.json' of 'diseases.json' weg. 
"""


def write_circlejson(dict, name):
    control_list = []
    child_dict = {}
    full_dict = {"name": "{}".format(name),
                 "children": []}
    for i in dict.keys():
        for j in dict[i].keys():

            if i not in control_list:

                control_list.append(i)
                child_dict = [{"name": j,
                               "size": dict[i][j]}]

            elif i in control_list:

                t = {"name": j,
                     "size": dict[i][j]}
                child_dict.append(t)

        full_dict["children"].append({"name": i, "children": child_dict})

    dic_tem = json.dumps(full_dict, indent=4)
    writetofile(dic_tem, name)


"""functie: Telt het aantal pubmedID's per combinatie van 
termen (obesitas en kinase, obesitas en gallic acid etc)
dict: een dictionary met hierin een dictionary {key 1 : {key 2 : [pubmedID's] } }. 
return: een dictionary met hierin een dictionary, 
de value is nu een integer van het aantal pubmedID's {key 1 : {key 2 : integer} }
"""


def set_value(dict):
    for i in dict.keys():
        key = i
        for j in dict[i].keys():
            dict[key][j] = len(dict[key][j])

    return dict


def writetofile(data, name):
    with open(definestaticpath() + '{}.json'.format(name), 'w') as file:
        file.write(data)
        file.close()

def openjson(name):
    path = definestaticpath()
    with open(path + '{}.json'.format(name)) as file:
        jsonobj = json.load(file)
    return jsonobj
def definestaticpath():
    path = "DataMiner/static/"
    return path
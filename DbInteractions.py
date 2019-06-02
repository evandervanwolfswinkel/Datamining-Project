from Bio import Entrez
from Bio import Medline
import importlib.util
import re
import mysql.connector.errors
import datetime
import json

Entrez.email = "anton.ligterink@gmail.com"


class DbInteractions:
    """Class for interactions with the MySQL database.
    Uses the MySqlCon class for connection establishing and
    the Article class for article processing.

    Usage
        Class initialisation                                        dbi = DbInteractions()

        Get the number of articles within the database              dbi.get_db_length()
        Get the number of relations within the database             dbi.get_relation_amount()
        Get the disease- and compound relation dictionaries         dbi.get_relations()
        Get a list of Article objects from the MySQL database       dbi.get_mysql_articles()
        Get lists of BG synonyms, compounds and diseases            dbi.get_lists()
        stored within the MySQL database

        After altering one or multiple disease/compound terms       dbi.update_relations()
        always update the relations
            Add term to diseases                                    dbi.add_rm('dis', term, True)
            Remove term from diseases                               dbi.add_rm('dis', term, False)
            Add term to compounds                                   dbi.add_rm('comp', term, True)
            Remove term from compounds                              dbi.add_rm('comp', term, False)

        After altering one or multiple Bitter gourd synonyms        dbi.renew_db()
        always renew the articles in the database.
        relations are updated automatically
            Add term to Bitter gourd synonyms                       dbi.add_rm('bg', term, True)
            Remove term from Bitter gourd synonyms                  dbi.add_rm('bg', term, False)

    """

    def __init__(self):
        """Constructor method for the DbInteractions class.
        """
        ms_spec = importlib.util.spec_from_file_location("MySqlCon.py", "MySqlCon.py")
        self.ms = importlib.util.module_from_spec(ms_spec)
        ms_spec.loader.exec_module(self.ms)

        article_spec = importlib.util.spec_from_file_location("Article.py", "Article.py")
        self.ar = importlib.util.module_from_spec(article_spec)
        article_spec.loader.exec_module(self.ar)

        self.synonyms, self.diseases_list, self.compound_list = [], [], []
        self.id_list, self.article_list = [], []
        self.dis_dict, self.comp_dict = {}, {}

    def renew_db(self):
        """Main method for renewing the database.
        Firstly downloads the Bitter gourd articles using the get_id_list() and get_articles() methods.
        Then resets the database using the reset_db() method.
        Afterwards the articles and relations are stored using the store_articles() and set_relations() methods.
        Finally the MySQL database connection is closed using the close() method from de mysqlCon class.
        """
        print(str(datetime.datetime.now()) + "\t\t\tRenewing database ...")
        self.get_lists()
        self.get_id_list()
        self.get_articles()
        self.reset_db()
        self.store_articles()
        self.set_relations()

    def update_relations(self):
        """Main method for updating the relations within the database.
        This method is used after altering the diseases and/or compound tables using add_rm().
        """
        self.get_lists()
        self.set_relations()

    def get_lists(self):
        """Method for retrieving the Bitter gourd synonym-, disease- and compound lists.
        Uses the MySqlCon class for establishing a connection to the database.
        @:return: synonyms(list):              List of synonyms for Bitter gourd
        @:return: disease_names(list):         List of disease names
        @:return: compound_names(list):        List of compound names
        """
        ms = self.ms.MySqlCon()
        rows = ms.execute_res("select * from bg_synonyms;")
        for synonym in rows:
            self.synonyms.append(synonym[0])
        rows = ms.execute_res("select * from disease_names;")
        for name in rows:
            self.diseases_list.append(name[0])
        rows = ms.execute_res("select * from compound_names;")
        for name in rows:
            self.compound_list.append(name[0])
        ms.close()
        print(str(datetime.datetime.now()) + "\t\t\tRetrieved BG synonyms, compounds and diseases")
        return self.synonyms, self.diseases_list, self.compound_list

    def get_id_list(self):
        """Method for generating a list of PubMed IDs associated with the different synonyms for Bitter gourd.
        Uses the get_synonym_ids() method to get an ID list of an individual synonym. Does this for every synonym,
        then creates a set of those lists.
        """
        for synonym in self.synonyms:
            self.id_list += self.get_synonym_ids(synonym)
        self.id_list = list(set(self.id_list))

    def get_synonym_ids(self, synonym):
        """Method for returning the corresponding id list for a synonym.
        @param        synonym: (str) synonym of Bitter gourd the PubMed database is searched for
        @return       id_list: (list) list of IDs the PubMed database returns when searched for synonym
        """
        handle = Entrez.esearch(db="pubmed", term=synonym, retmax=999999999)
        record = Entrez.read(handle)
        handle.close()
        return list(record["IdList"])

    def get_articles(self):
        """Method for acquiring the articles corresponding to PubMed IDs in id_list.
        Articles without either a title, abstract, year or PubMed ID are not stored in the database.
        The generated Article objects are stored within the article_list(list).
        """
        handle = Entrez.efetch(db="pubmed", id=self.id_list, rettype="medline", retmode="json")
        records = Medline.parse(handle)
        for record in records:
            try:
                article = self.ar.Article(record['TI'].replace("'", "\\\'"), record['AB'].replace("'", "\\\'"),
                                          record['DP'][0:4], record['PMID'])
                self.article_list.append(article)
            except KeyError:
                pass
        print(str(datetime.datetime.now()) + "\t\t\tArticles acquired")

    def store_articles(self):
        """Method for storing articles in the MySQL database.
        Uses the Article objects within the article_list(list) to generate a MySQL query
        in order to fill the articles table.
        """
        query = "INSERT INTO articles(pubmed_id, title, abstract, year_published) VALUES"
        for article in self.article_list:
            query += str("(" + str(article.get_pubmed_id()) + ",\'" + article.get_title() + "\',\'" +
            article.get_abstract() + "\'," + str(article.get_year()) + "),")
        query = query[:-1]+";"
        ms = self.ms.MySqlCon()
        ms.execute_no_res(query)
        ms.close()
        print(str(datetime.datetime.now()) + "\t\t\tArticles set, now holding "
              + str(self.get_db_length()) + " articles")

    def set_relations(self):
        """Method for storing relations between articles in the MySQL database.
        Uses the search_relations() method to search for terms within an article.
        Uses the self.article_list(list) to store relations within the self.diseases_list(list) and
        the self.compound_list(list).
        """
        dis_query = "INSERT INTO diseases(dis_name, title_bool, abstract_bool, pmid_fk) VALUES"
        comp_query = "INSERT INTO compounds(comp_name, title_bool, abstract_bool, pmid_fk) VALUES"
        if not self.article_list:
            self.get_mysql_articles()

        for article in self.article_list:
            for term in self.diseases_list:
                title_bool, abstract_bool = self.search_relations(term, article)
                if any([title_bool, abstract_bool]):
                    dis_query += str("(\'"+term+"\',"+str(title_bool)+","+str(abstract_bool)+
                                     ","+str(article.get_pubmed_id())+"),")
            for term in self.compound_list:
                title_bool, abstract_bool = self.search_relations(term, article)
                if any([title_bool, abstract_bool]):
                    comp_query += str("(\'"+term+"\',"+str(title_bool)+","+str(abstract_bool)+
                                      ","+str(article.get_pubmed_id())+"),")

        dis_query = dis_query[:-1]+";"
        comp_query = comp_query[:-1]+";"
        self.clear_dis_comp_tables()

        ms = self.ms.MySqlCon()
        ms.execute_no_res(dis_query)
        ms.execute_no_res(comp_query)
        ms.close()
        print(str(datetime.datetime.now()) + "\t\t\tRelations set, now holding " +
              str(self.get_relation_amount()) + " relations")

    def clear_dis_comp_tables(self):
        """Method for clearing the disease_names and compound_names tables.
        """
        ms = self.ms.MySqlCon()
        ms.execute_no_res('SET FOREIGN_KEY_CHECKS = 0;')
        ms.execute_no_res('TRUNCATE TABLE diseases;')
        ms.execute_no_res('truncate table compounds;')
        ms.execute_no_res('SET FOREIGN_KEY_CHECKS = 1;')
        ms.close()

    def search_relations(self, term, article):
        """Method for locating a term within an article.
        :param   term:          a word to be searched for within the article's title and abstract.
        :param   article:       instance of the Article class containing the title, year, abstract and PubMed
                                ID of an article.
        :return: title_bool:    boolean indicating whether a term occurs within the title of an article.
        :return: abstract_bool: boolean indicating whether a term occurs within the abstract of an article.
        """
        title = re.sub(r'\W+', '', article.get_title().lower())
        abstract = re.sub(r'\W+', '', article.get_abstract().lower())
        term = re.sub(r'\W+', '', term.lower())
        title_bool = bool(re.search(term.lower(), title))
        abstract_bool = bool(re.search(term.lower(), abstract))
        return title_bool, abstract_bool

    def reset_db(self):
        """Method for resetting the articles, diseases and compounds tables.
        Uses the MySqlCon class for database interactions.
        """
        ms = self.ms.MySqlCon()
        ms.execute_no_res("SET FOREIGN_KEY_CHECKS = 0;")
        ms.execute_no_res("TRUNCATE TABLE articles;")
        ms.execute_no_res("TRUNCATE TABLE diseases;")
        ms.execute_no_res("TRUNCATE TABLE compounds;")
        ms.execute_no_res("SET FOREIGN_KEY_CHECKS = 1;")
        ms.close()
        print(str(datetime.datetime.now()) + "\t\t\tDatabase reset")

    def get_db_length(self):
        """
        Method for calculating and returning the database length.
        :return:     database_length(int)
        """
        ms = self.ms.MySqlCon()
        return ms.execute_res("select count(*) from articles;")[0][0]

    def get_relation_amount(self):
        """
        Method for calculating and returning the amount of relations within the MySQL database.
        :return:     database_length(int)
        """
        ms = self.ms.MySqlCon()
        return ms.execute_res("""select count(*) 
            from diseases d inner join compounds c on d.pmid_fk = c.pmid_fk;""")[0][0]

    def get_relations(self):
        """Method for retrieving the relations between diseases and compounds and storing them in dictionaries.
        Retrieves the relations from the database using the MySqlCon class, then stores the relations within
        self.dis_dict and self.comp_dict.

        :return:
        """
        ms = self.ms.MySqlCon()
        rows = ms.execute_res("""select d.dis_name, c.comp_name, c.pmid_fk 
                            from diseases d inner join compounds c on d.pmid_fk = c.pmid_fk;""")
        ms.close()

        for row in rows:
            if row[0] not in self.dis_dict:
                self.dis_dict[row[0]] = {row[1]: [row[2]]}
            elif row[1] not in self.dis_dict.get(row[0]):
                self.dis_dict[row[0]][row[1]] = [row[2]]
            elif row[2] not in self.dis_dict[row[0]][row[1]]:
                self.dis_dict[row[0]][row[1]].append(row[2])

            if row[1] not in self.comp_dict:
                self.comp_dict[row[1]] = {row[0]: [row[2]]}
            elif row[0] not in self.comp_dict.get(row[1]):
                self.comp_dict[row[1]][row[0]] = [row[2]]
            elif row[2] not in self.comp_dict[row[1]][row[0]]:
                self.comp_dict[row[1]][row[0]].append(row[2])
        return self.dis_dict, self.comp_dict

    def add_rm(self, table, value, add_or_rm):
        if add_or_rm:
            query = "INSERT INTO placeholder VALUES(\'"
        elif not add_or_rm:
            query = "DELETE FROM placeholder WHERE (name) IN (\'"
        try:
            ms = self.ms.MySqlCon()
            query += str(value + "\');")
            if table == 'bg':
                ms.execute_no_res(str(query.replace('placeholder', 'bg_synonyms')))
            elif table == 'dis':
                ms.execute_no_res(str(query.replace('placeholder', 'disease_names')))
            elif table == 'comp':
                ms.execute_no_res(str(query.replace('placeholder', 'compound_names')))
            ms.close()
            if add_or_rm:
                print(str(datetime.datetime.now()) + "\t\t\tNew term in \'" + table + "\': \'" + value + "\'")
            if not add_or_rm:
                print(str(datetime.datetime.now()) + "\t\t\tTerm deleted from \'" + table + "\': \'" + value + "\'")
        except mysql.connector.errors.ProgrammingError:
            print("Empty list/programming error")
            ms.close()
        except mysql.connector.errors.IntegrityError:
            print(str(datetime.datetime.now()) + "\t\t\tDuplicate term in \'" + table + "\': \'" + value + "\'")
            ms.close()

    def get_mysql_articles(self):
        """Method for retrieving all articles from the MySQL database.
        Uses the MySqlCon class for connection establishing.
        :return: article_list(list): list of Article objects retrieved from the MySQL database
        """
        ms = self.ms.MySqlCon()
        rows = ms.execute_res('SELECT * FROM articles;')
        ms.close()
        for row in rows:
            article = self.ar.Article(pubmed_id=row[0], title=row[1], abstract=row[2], year=row[3])
            self.article_list.append(article)
        print(str(datetime.datetime.now()) + "\t\t\tRetrieved articles from MySQL database")
        return self.article_list

    def return_article_dict(self, dict_type):
        """Method for creating a dictionary of all article information for site use by JSON format
        :return: tempjson(dict): dictionary of articles in JSON format
        """
        articles = self.get_mysql_articles()
        tempdict = {}
        for p_id, p_info in dict_type.items():
            for key in p_info:
                for value in p_info[key]:
                    for article in articles:
                        if str(value) == str(article.pubmed_id):
                            title = str(p_id) + " - " + str(article.get_title())
                            tempdict[value] = [title, article.get_year(), article.get_abstract(), article.get_pubmed_id(), key]
        self.tempjson = json.dumps(tempdict, indent=4)
        return self.tempjson

    def return_json_termlist(self, term_list):
        """Method for creating a JSON list from a term_list
        :return: tempjson(list): list of searchterms in JSON
        """
        self.tempjson = json.dumps(term_list)
        return self.tempjson








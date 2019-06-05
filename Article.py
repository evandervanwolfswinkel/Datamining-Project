class Article:
    """
        @:Author: Anton Ligterink
        @:Function: Class for storing articles within an object.
    """

    def __init__(self, title, abstract, year, pubmed_id):
        """Constructor method for the Article class.
        :param title: (str) title of the article, max length is 250 characters
        :param abstract: (str) abstract of the article, max length is 10.000 characters
        :param year: (int) year when article was published, max length is 4 integers
        :param pubmed_id: (int) PubMed ID belonging to the article, max length is 8 characters
        """
        self.title = title
        self.abstract = abstract
        self.year = int(year)
        self.pubmed_id = int(pubmed_id)

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title

    def get_abstract(self):
        return self.abstract

    def set_abstract(self, abstract):
        self.abstract = abstract

    def get_year(self):
        return self.year

    def set_year(self, year):
        self.year = year

    def get_pubmed_id(self):
        return self.pubmed_id

    def set_pubmed_id(self, pubmed_id):
        self.pubmed_id = pubmed_id

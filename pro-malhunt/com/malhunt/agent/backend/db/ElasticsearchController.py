import os
import  datetime
from ElasticsearchClientCreator import ElasticsearchclientCreator
from com.malhunt.agent.backend.model.SearchItem import SearchItem
import configparser

class ESController(object):

    def __init__(self):
        self.es_client = ElasticsearchclientCreator().getClient()
        self.config = configparser.ConfigParser()
        self.config.readfp(open(os.path.dirname(__file__) + '/../config/mhprop.ini'))

    def insertItem(self, filename):
        item = SearchItem(id = filename, name = os.path.basename(filename), type = 'file', ingestion_date = datetime.datetime.today(), md5 = None)
        res = self.es_client.index(index=self.config['DEFAULT']['index'], doc_type=self.config['DEFAULT']['type'], id=item.id, body=vars(item))
        return  res

    def getItem(self, name):
        res = self.es_client.search(index=self.config['DEFAULT']['index'], body = {'query':{'match':{'name':"'"+name+"'"}}})['hits']['total']
        return res


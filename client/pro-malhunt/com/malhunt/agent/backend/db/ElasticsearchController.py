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

    def insertItem(self, name, type, id=None):
        if type=='file':
            id=name
            name=os.path.basename(name)
        elif type=='proc':
            pass
        item = SearchItem(id=id, name=name, type=type,
                          ingestion_date=datetime.datetime.today(), md5=None)
        return self.es_client.index(index=self.config['DEFAULT']['index'], doc_type=self.config['DEFAULT']['type'], id=item.id, body=vars(item))

    #TODO: Note that 'name' param here for files refers to the whole path (The full qualified file name)
    def purgeItem(self, name, type, id=None):
        if type=='file':
            id = name  #The full qualified name is being used as id for files
        elif type=='proc':
            id = id

        return self.es_client.delete(index=self.config['DEFAULT']['index'], doc_type=self.config['DEFAULT']['type'], id=id)


    def getItem(self, name):
        res = self.es_client.search(index=self.config['DEFAULT']['index'], body = {'query':{'match':{'name':"'"+name+"'"}}})['hits']['total']
        return res


import os
import  datetime
from ElasticsearchClientCreator import ElasticsearchclientCreator
from com.malhunt.agent.backend.model.SearchItem import SearchItem
import configparser
import json
import sys

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
                          ingestion_date=datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'), md5=None)
        return self.es_client.index(index=self.config['DEFAULT']['index'], doc_type=self.config['DEFAULT']['type'], id=item.id, body=vars(item))

    #TODO: Note that 'name' param here for files refers to the whole path (The full qualified file name)
    def purgeItem(self, name, type, id=None):
        if type=='file':
            id = name  #The full qualified name is being used as id for files
        elif type=='proc':
            id = id

        return self.es_client.delete(index=self.config['DEFAULT']['index'], doc_type=self.config['DEFAULT']['type'], id=id)


    def checkItem(self, name):
        res = self.es_client.search(index=self.config['DEFAULT']['index'], body = {'query':{'term':{'name':name}}}, size=self.config['DEFAULT']['es_limit'], from_=0)
        return res['hits']['total']

    def fuzzyCheckItem(self, regex):
        res = self.es_client.search(index=self.config['DEFAULT']['index'], body = {"query": {"query_string":{"allow_leading_wildcard":True,"default_field": "name","query": regex}}}, size=self.config['DEFAULT']['es_limit'], from_=0)['hits']['total']
        return res['hits']['total']

    def getItem(self, name):
        res = self.es_client.search(index=self.config['DEFAULT']['index'], body={'query': {'term': {'name': name}}}, size=self.config['DEFAULT']['es_limit'], from_=0)
        return self.getHitsListFromESResult(res)

    def fuzzyGetItem(self, regex):
        res = self.es_client.search(index=self.config['DEFAULT']['index'], body={
            "query": {"query_string": { "allow_leading_wildcard": True, "default_field": "name", "query": regex}}}, size=self.config['DEFAULT']['es_limit'], from_=0)
        return self.getHitsListFromESResult(res)

    def getHitsListFromESResult(self, res):
        hits = []
        for hit in res['hits']['hits']:
            hits.append({'name': hit['_source']['name'], 'id': hit['_source']['id']})
        return hits


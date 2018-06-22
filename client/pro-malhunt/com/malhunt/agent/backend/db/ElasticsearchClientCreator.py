import elasticsearch
import configparser
import os

class ElasticsearchclientCreator(object):
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.readfp(open(os.path.dirname(__file__) + '/../config/mhprop.ini'))

        self.es_client = elasticsearch.Elasticsearch(
            hosts=[{'host': self.config['DEFAULT']['host'], 'port': int(self.config['DEFAULT']['port'])}],
            sniff_on_start=bool(self.config['DEFAULT']['sniff_on_start']),
            sniff_on_connection_fail=bool(self.config['DEFAULT']['sniff_on_connection_fail']),
            sniffer_timeout=int(self.config['DEFAULT']['sniffer_timeout']))

    def getClient(self):
        return self.es_client


#res = es.index(index=config['DEFAULT']['index'], doc_type=config['DEFAULT']['type'], id=2, body=e1)
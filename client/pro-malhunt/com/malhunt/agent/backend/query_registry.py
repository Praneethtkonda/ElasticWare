import os
import re
from com.malhunt.agent.backend.db.ElasticsearchController import ESController

def search_registry(key):
    es_handle = ESController()
    return es_handle.fuzzyGetItem(regex=key, type='file')

if __name__ == '__main__':
	print(search_registry('Elements'))
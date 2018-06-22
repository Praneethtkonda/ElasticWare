import os
import re
from com.malhunt.agent.backend.db.ElasticsearchController import ESController

'''
SAMPLE FILE TO STORE REGISTRY KEYS
FOR NOW WE'LL USE FILE INSTEAD OF DB
'''


def search_registry(key):
    es_handle = ESController()
    if es_handle.getItem(key) > 0:
        return True

if __name__ == '__main__':
	print(search_registry('Elements'))
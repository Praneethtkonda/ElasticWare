from com.malhunt.agent.backend.db.ElasticsearchController import ESController

class md5_api(object):
    '''
    	md5_api allows agent to access process related operations
    '''

    es_handle = ESController()

    def __init__(self):
        pass

    def check_md5(self, md5):
        return self.es_handle.fuzzyCheckItem(regex=md5, type='md5')

    def get_md5(self, md5):
        return self.es_handle.fuzzyGetItem(regex=md5, type='md5')
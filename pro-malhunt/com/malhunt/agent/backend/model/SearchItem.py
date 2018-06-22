
class SearchItem(object):
    def __init__(self):
        self.id = None
        self.name = None
        self.type = None
        self.ingestion_date = None
        self.md5 = None

    def __init__(self, id = None, name = None, type = None, ingestion_date = None ,md5 = None):
        self.id = id
        self.name = name
        self.type = type
        self.ingestion_date = ingestion_date
        self.md5 = md5


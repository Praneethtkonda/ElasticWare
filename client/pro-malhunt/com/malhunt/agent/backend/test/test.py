
from com.malhunt.agent.backend.db.ElasticsearchController import ESController

es_handle = ESController()
with open('C:\Users\qauser\Downloads\wfile.txt') as fin:
    for line in fin:
        print es_handle.insertItem(line.strip())
# if es_handle.getItem('mso30win32client.dll') >0:
#     print('FOUND!!!')
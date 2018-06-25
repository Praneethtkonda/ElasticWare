
from com.malhunt.agent.backend.db.ElasticsearchController import ESController

es_handle = ESController()
# with open('C:\Users\qauser\Downloads\wfile.txt') as fin:
#     for line in fin:
#         print es_handle.insertItem(line.strip(), 'file')
# if es_handle.getItem('mso30win32client.dll') >0:
#     print('FOUND!!!')

print es_handle.insertItem('C:/swapfile.sys', 'file')
print es_handle.getItem('swapfile.sys')
print es_handle.purgeItem('C:/swapfile.sys', 'file')
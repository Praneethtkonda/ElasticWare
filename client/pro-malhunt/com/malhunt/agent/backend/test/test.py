
from com.malhunt.agent.backend.db.ElasticsearchController import ESController

es_handle = ESController()
'''with open('C:\Users\qauser\Downloads\wfile.txt') as fin:
    for line in fin:
        try:
            print es_handle.insertItem(line.strip(), 'file')
        except Exception as e:
            print 'Skipping file:{}, insertion call caused exception:{}'.format(line.strip(),str(e))'''

# if es_handle.getItem('hiberfil.sys') >0:
#      print('FOUND!!!')

#print es_handle.insertItem('C:/swapfile.sys', 'file')
# print es_handle.getItem('swapfile.sys')
# print es_handle.purgeItem('C:/swapfile.sys', 'file')

# obj = es_handle.getItem('swapfile.sys')
# print 'Name: {}, Type: {}'.format(obj['name'], obj['type'])
print es_handle.fuzzyGetItem(regex="*", type='file')
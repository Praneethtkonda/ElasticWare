import query_registry
from socketIO_client import SocketIO
import unicodedata
import json
import socket
from process import proc_api

socketIO = SocketIO('10.33.35.132', 3000)


def find_in_system(message):
    #TODO: @Rittwik/@Srisannidhi Change this workaround to something more maintainable.
    if type(message) == unicode:
        message = unicodedata.normalize('NFKD', message.strip()).encode('ascii', 'ignore')
        message_json = json.loads(message)
        search_formats = {
            'file': query_registry.search_registry,
            'reg': None,
            'proc': proc_api.proc_api().check_process,
            'md5': None}
        isReg = 'Yes' if search_formats[message_json['request_type']](message_json['name']) else 'No'
        socketIO.emit('message', json.dumps({'result':isReg, 'hostname':socket.gethostname(), 'name':message_json['name']}))

def main():
	socketIO.on('message', find_in_system)
	socketIO.wait()
	
if __name__ == '__main__':
	main()
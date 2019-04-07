#LET's SEE IF THIS SHOWS UP

from socketIO_client import SocketIO
import unicodedata
import json
import socket
from process import proc_api
from file import file_api
from md5 import md5_api
from threading import Thread
import callback_all
from registry import registry_api
socketIO = SocketIO('10.33.34.229', 3000)


def find_in_system(message):
    #TODO: @Rittwik/@Srisannidhi Change this workaround to something more maintainable.
    if type(message) == unicode:
        message = unicodedata.normalize('NFKD', message.strip()).encode('ascii', 'ignore')
        message_json = json.loads(message)
        search_formats = {
            'file': file_api.FileEventsHandler().get_files,
            'reg': registry_api.registry_api().check_registry,
            'proc': proc_api.proc_api().get_process,
            'md5': md5_api.md5_api().get_md5
            }

        response = search_formats[message_json['request_type']](message_json['name'])
        socketIO.emit('message', json.dumps({'hostname':socket.gethostname(), 'response':response, 'request':message_json['name']}))

def main():
	update_obj = Thread(target = callback_all.init)
	update_obj.start()
	socketIO.on('message', find_in_system)
	socketIO.wait()
	update_obj.join()
	
if __name__ == '__main__':
    main()
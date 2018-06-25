import query_registry
from socketIO_client import SocketIO
import unicodedata

socketIO = SocketIO('10.33.34.130', 3000)


def find_in_system(message):
    #TODO: @Rittwik/@Srisannidhi Change this workaround to something more maintainable.
    if type(message) == unicode:
        message = unicodedata.normalize('NFKD', message.strip()).encode('ascii', 'ignore')
        isReg = 'Yes' if query_registry.search_registry(message) else 'No'
        socketIO.emit('message', '{}: {}'.format(message, isReg))

def main():
	socketIO.on('message', find_in_system)
	socketIO.wait()
	
if __name__ == '__main__':
	main()
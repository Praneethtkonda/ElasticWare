import query_registry
from socketIO_client import SocketIO

socketIO = SocketIO('10.33.34.19', 3000)


def find_in_system(message):
	print 'Hello'
	if type(message) == type('a'):
		isReg = 'Yes' if query_registry.search_registry(message) else 'No'
		socketIO.emit('message', '{}: {}'.format(message, isReg))

def main():
	socketIO.on('message', find_in_system)
	socketIO.wait()
	
if __name__ == '__main__':
	main()
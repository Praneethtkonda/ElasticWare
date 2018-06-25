from socketIO_client import SocketIO
def message_response(data):
	if type(data) == type('a'):
		print(data)
		print(type(data))
	
#Write the addition code from here


#To here
socketIO = SocketIO('localhost', 3000)
mess = 'Example Message'
# Listen

socketIO.emit('message',mess)

#socketIO.wait(seconds=7)
socketIO.on('message', message_response)

socketIO.wait()
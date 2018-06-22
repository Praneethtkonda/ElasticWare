from socketIO_client import SocketIO
def message_response(data):
	if type(data) == type('a'):
		print(data)
	
#Write the addition code from here


#To here
socketIO = SocketIO('10.33.34.19', 3000)
mess = 'Example Message'
# Listen

socketIO.emit('message',mess)

#socketIO.wait(seconds=7)
socketIO.on('message', message_response)

# socketIO.wait()
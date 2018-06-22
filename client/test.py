from socketIO_client import SocketIO
def message_response(data):
    print(data)
#Write the addition code from here

#To here
socketIO = SocketIO('localhost', 3000)
mess = 'Hi praneeth'
# Listen

socketIO.emit('message',mess)

#socketIO.wait(seconds=7)
socketIO.on('message', message_response)

socketIO.wait()
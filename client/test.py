from socketIO_client import SocketIO
def message_response(data):
    print(data)

socketIO = SocketIO('localhost', 3000)
mess = 'Hi praneeth'
# Listen

socketIO.emit('message',mess)

#socketIO.wait(seconds=7)
socketIO.on('message', message_response)

socketIO.wait()
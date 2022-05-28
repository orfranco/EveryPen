import socketio


class Client:
    """
    This is the client class that will activate update_values method on
    'recieved_data' event.
    """
    def __init__(self, host, port, update_values):
        self.host = host
        self.port = port
        self.sio = socketio.Client()
        self.sio.connect(f'http://{self.host}:{self.port}')
        self.sio.on('recieve-data', self.on_message)
        self.update_values = update_values

    def on_message(self, data):
        self.update_values(data)

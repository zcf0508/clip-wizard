import argparse
import multiprocessing
import socket

import webview

from server import app


def get_free_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port

SERVER_PORT = get_free_port()
CLIENT_PORT = 12333

class Api():
    def get_server_port(self):
        """
        Expose the server-side port number to the client, return the port of the server
        """
        return SERVER_PORT

def run_app():
    """
    Run the server in a separate process
    """
    app.run(port=SERVER_PORT)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dev", action=argparse.BooleanOptionalAction, help="if_cef")
    args = parser.parse_args()
    
    DEV_MODE = True if args.dev else False

    if DEV_MODE:
        multiprocessing.Process(target=run_app).start()
    else:
        app.config.setdefault('SERVER_NAME', 'localhost:%s' % SERVER_PORT)

    webview.create_window(
        title='Hello world', 
        url=f'http://localhost:{CLIENT_PORT}/' if DEV_MODE else app,
        confirm_close=True,
        js_api=Api()
    )
    webview.start(debug=DEV_MODE)

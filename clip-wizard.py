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
DEV_SERVER_PORT = 13444
CLIENT_PORT = 12333

class Api():
    def get_server_port(self):
        """
        Expose the server-side port number to the client, return the port of the server
        """
        return SERVER_PORT

def run_app(port):
    """
    Run the server in a separate process
    """
    app.run(port=port)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dev", action=argparse.BooleanOptionalAction, help="if_cef")
    args = parser.parse_args()
    
    DEV_MODE = True if args.dev else False

    if DEV_MODE:
        multiprocessing.Process(
            target=run_app, 
            args=(DEV_SERVER_PORT if DEV_MODE else SERVER_PORT,)
        ).start()
    else:
        app.config.setdefault('SERVER_NAME', 'localhost:%s' % SERVER_PORT)

    webview.create_window(
        title='Clip Wizard', 
        url=f'http://localhost:{CLIENT_PORT}/' if DEV_MODE else app,
        confirm_close=False if DEV_MODE else True,
        js_api=Api()
    )
    webview.start(debug=DEV_MODE)

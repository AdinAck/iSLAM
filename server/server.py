"""
Structure(s) for the SLAM server.

Adin Ackerman
"""

import logging
from utils import Triple
from websocket_server import WebsocketServer


class SlamServer(WebsocketServer):
    """
    A websocket server for encapsulating position and orientation data
    as well as, of course, facilitating the websocket.
    """

    pos: Triple[float] = Triple(0., 0., 0.)
    rot: Triple[float] = Triple(0., 0., 0.)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_fn_message_received(self.msg_recv)

    def msg_recv(self, client, server: WebsocketServer, message: str) -> None:
        """
        Callback for when we receive a message from the phone.
        """

        data = list(map(float, message.split(',')))

        self.pos = Triple(*data[:3])
        self.rot = Triple(*data[3:])


def main():
    server = SlamServer(host='0.0.0.0', port=8080, loglevel=logging.INFO)
    server.run_forever()


if __name__ == '__main__':
    main()

from typing import Optional

from pythonosc import osc_server, udp_client
from pythonosc.dispatcher import Dispatcher

__all__ = ["OscIn", "OscOut"]


# (server)
class OscIn:
    def __init__(self, ip: str, port: int):
        self._ip = ip
        self._port = port
        self._dispatcher = Dispatcher()
        self._server: osc_server.ThreadingOSCUDPServer

        self.map = self._dispatcher.map

    def ip(self) -> str:
        """
        Returns the ip the server is listening on.
        """
        return self._ip

    def port(self) -> int:
        """
        Returns the port the server is listening on.
        """
        return self._port

    def server(self) -> Optional[osc_server.ThreadingOSCUDPServer]:
        """
        Returns the internal osc server.
        """
        return self._server

    def start(self):
        """
        Starts listening to incoming osc messages.
        """
        self._server = osc_server.ThreadingOSCUDPServer(
            (self._ip, self._port), self._dispatcher
        )
        self._server.serve_forever()


# (client)
class OscOut:
    def __init__(self, ip: str = "127.0.0.1", port: int = 5005):
        self._client = udp_client.SimpleUDPClient(ip, port)
        self._ip = ip
        self._port = port

        self.send_message = self._client.send_message

    def ip(self) -> str:
        """
        Returns the client's ip.
        """
        return self._ip

    def port(self) -> int:
        """
        Returns the client's port.
        """
        return self._port

    def client(self) -> udp_client.SimpleUDPClient:
        """
        Returns the internal client.
        """
        return self._client

from pythonosc import osc_server, udp_client
from pythonosc.dispatcher import Dispatcher

__all__ = ["OscIn", "OscOut"]


# (server)
class OscIn:
    def __init__(self, ip: str, port: int):
        self._ip = ip
        self._port = port
        self._dispatcher = Dispatcher()
        self._server = osc_server.ThreadingOSCUDPServer(
            (self._ip, self._port), self._dispatcher
        )

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

    # def map(self, address: str, callback, ):
    #     self._dispatcher.map


# (client)
class OscOut:
    def __init__(self):
        pass

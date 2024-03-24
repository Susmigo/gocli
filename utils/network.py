import requests

from utils.display import Display


class NetworksOps:
    """
    This class contains the network check methods.
    """

    def __init__(self):
        self.display = Display()

    def checkNetwork(self) -> bool:
        """
        Checks whether there is a network or not.

        :returns: bool
        """
        try:
            response = requests.get("http://www.google.com", timeout=5)
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.ConnectionError as e:
            self.display.error_Exit("No Network. Connect to any and try again.", trace=str(e))


if __name__ == "__main__":
    nops = NetworksOps()
    print(nops.checkNetwork())

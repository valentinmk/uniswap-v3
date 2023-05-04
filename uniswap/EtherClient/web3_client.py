from typing import Optional
from web3 import Web3
from web3.providers.rpc import HTTPProvider
from web3.providers.async_rpc import AsyncHTTPProvider
from web3.providers.websocket import WebsocketProvider
from web3.eth import AsyncEth


class EtherClient:
    """
    Client helper to connect to with interact with the Ethereum blockchain.
    It should work with all supported blockchains under web3.py.

    Parameters
    ----------
    http_url : str
        URL for HTTPProvider. Required, if `ws_url` not provided.
    ws_url : str, optional
        URL for WSProvider. Required, if `http_url` not provided.
    http_async : bool, optional, default = False
        True for use AsyncHTTPProvider instead of HTTPProvider.
        By default is False.
    my_address : str, optional
        Address of the wallet
    my_wallet_pass : str, optional
        Password for the wallet
    my_keyfile_json : str, optional
        Secret file encrypted with `my_wallet_pass`

    Attributes
    ----------
    url : str, optional
        URL for web3.providers.rpc.HTTPProvider. Required, if `ws_url` not provided.
    ws_url : str, optional
        URL for web3.providers.rpc.WSProvider. Required, if `url` not provided.
    http_async: bool, default=False
        True for use AsyncHTTPProvider instead of HTTPProvider.
    address: str
        Address of the wallet
    _wallet_pass : str, optional
        Password for the wallet
    _keyfile_json : json, optional
        Secret file encrypted with self._wallet_pass
    _w3 : web3.Web3
        web3.Web3 instance to interact with the Ethereum blockchain.

    Returns
    -------
    EtherClient
    """

    def __init__(
        self,
        http_url: str = None,
        ws_url: str = None,
        http_async: bool = False,
        my_address: str = None,
        my_wallet_pass: str = None,
        my_keyfile_json: str or dict = None,
    ) -> None:
        self.url: str = http_url
        self.ws_url: str = ws_url
        self.http_async: str = http_async
        self.address: str = my_address
        # private
        self._wallet_pass: str = my_wallet_pass
        self._keyfile_json: str | dict = my_keyfile_json

        self._w3: Optional[Web3] = None

    def init_w3(self) -> Web3:
        """Invoke and return an web3.Web3 instance."""
        if self.url is not None:
            if self.http_async is True:
                return Web3(
                    AsyncHTTPProvider(self.url),
                    modules={"eth": (AsyncEth,)},
                    middlewares=[],
                )
            else:
                return Web3(HTTPProvider(self.url))
        elif self.ws_url is not None:
            return Web3(WebsocketProvider(self.ws_url))
        else:
            raise BaseException("unable to define Ether Provider")
            return None

    @property
    def w3(self) -> Web3:
        """Web3: web3.Web3 instance to interact with the Ethereum blockchain."""
        if self._w3 is None:
            self._w3 = self.init_w3()
        return self._w3

from typing import Optional
from web3 import Web3
from web3.providers.rpc import HTTPProvider
from web3.providers.async_rpc import AsyncHTTPProvider
from web3.providers.websocket import WebsocketProvider
from web3.eth import AsyncEth


class EtherClient:
    """
    Client helper for connect to blockchain.
    It should work with all supported blockchains under web3.py.

    Parameters
    ----------
    http_url : str
        [Optional] url for HTTPProvider. Required, if `ws_url` not provided.
    ws_url : str
        [Optional] url for WSProvider. Required, if `http_url` not provided.
    http_async : bool
        [Optional] True for use AsyncHTTPProvider instead of HTTPProvider.
        By default is False.
    my_address : str
        [Optional] Address of the wallet
    my_wallet_pass : str
        [Optional] Password for the wallet
    my_keyfile_json : str
        [Optional] Secret file encrypted with `my_wallet_pass`

    Returns
    -------
    EtherClient
    """

    def __init__(
        self,
        http_url: str = None,
        ws_url: str = None,
        http_async=False,
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
        if self._w3 is None:
            self._w3 = self.init_w3()
        return self._w3

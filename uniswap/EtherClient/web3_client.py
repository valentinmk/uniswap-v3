from typing import Optional
from web3 import Web3
from web3.providers.rpc import HTTPProvider
from web3.providers.async_rpc import AsyncHTTPProvider
from web3.providers.websocket import WebsocketProvider


class EtherClient:
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
                return Web3(AsyncHTTPProvider(self.url))
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

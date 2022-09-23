from eth_typing import ChecksumAddress
from web3 import Web3

from .base import BaseContract


class SwapRouter(BaseContract):
    def __init__(
        self,
        w3: Web3,
        address: ChecksumAddress,
        abi_path: str = "../utils/abis/swap_router.abi.json",
    ):
        super().__init__(w3, address, abi_path)
        self._data = None

    def _get_data(self):
        return "Dummy"

    @property
    def data(self):
        """Get human readable information from pool"""
        if self._data is None:
            self._data = self._get_data()
        return self._data

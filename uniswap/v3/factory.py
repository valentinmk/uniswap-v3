from eth_typing import ChecksumAddress
from web3 import Web3
from .base import BaseContract


class Factory(BaseContract):
    def __init__(
        self,
        w3: Web3,
        address: ChecksumAddress,
        abi_path: str = "../utils/abis/factory.abi.json",
    ):
        super().__init__(w3, address, abi_path)

import json
import os

from eth_typing import ChecksumAddress
from web3 import Web3
from web3.contract import Contract, ContractFunctions

# from ..utils.consts import CONTRACT_ADDRESSES


class BaseContract:
    def __init__(self, w3: Web3, address: ChecksumAddress, abi_path: str) -> None:
        self.w3 = w3
        self.address: ChecksumAddress = address
        self.abi_path: str = abi_path
        self._contract: Contract = None

    def init_contract(self, address: ChecksumAddress, path: str) -> Contract:
        abi_file = open(f"{os.path.dirname(__file__)}/{path}")
        abi = json.load(abi_file)
        return self.w3.eth.contract(address=address, abi=abi)

    @property
    def contract(self) -> Contract:
        """Returns contract instance"""
        if self._contract is None:
            self._contract = self.init_contract(self.address, self.abi_path)
            self.address = self._contract.address
        return self._contract

    @property
    def functions(self) -> ContractFunctions:
        """Quick access to `self.contract.functions`"""
        contract = self.contract
        return contract.functions

    def get_functions(self) -> list:
        """List all smart contract available functions"""
        return [
            i
            for i in self.contract.functions.__dir__()
            if not i.startswith("__")
            and (i not in ["abi", "web3", "address", "_functions", "parameters"])
        ]

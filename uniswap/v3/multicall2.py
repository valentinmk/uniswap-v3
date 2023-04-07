from dataclasses import dataclass
from typing import List

from eth_abi import decode
from eth_typing import ChecksumAddress

# from hexbytes import HexBytes
from uniswap.EtherClient.web3_client import EtherClient
from web3 import Web3

# from web3.types import TxReceipt
from web3.contract.contract import ContractFunction

from .base import BaseContract


@dataclass
class Call:
    func_call: ContractFunction
    name: str = ""
    returns: list[tuple] = None
    outputs: list[dict] = None
    block_number: int = 0


class Multicall2(BaseContract):
    def __init__(
        self,
        client: EtherClient,
        w3: Web3,
        address: ChecksumAddress,
        abi_path: str = "../utils/abis/multicall2.abi.json",
    ):
        super().__init__(w3, address, abi_path)
        self.client = client
        self._data = None

    def _get_data(self):
        raise NotImplementedError

    def aggregate_and_call(self, functions: List[ContractFunction]) -> List[Call]:
        calls: List[Call] = [Call(func_call=func) for func in functions]
        for func_call, call in zip(calls, functions):
            func_call.outputs = call.abi["outputs"]  # to trough exception
            func_call.name = call.fn_name
        multicall2_call: ContractFunction = self.functions.aggregate(
            [
                {
                    "target": call.func_call.address,
                    "callData": call.func_call._encode_transaction_data(),
                }
                for call in calls
            ]
        )
        block_number, results = multicall2_call.call()
        for call, result in zip(calls, results):
            list_of_typ = [i["type"] for i in call.outputs]
            # typ = f"({','.join(list_of_typ)})"
            call.returns = decode(types=list_of_typ, data=result)
            call.block_number = block_number
        return calls

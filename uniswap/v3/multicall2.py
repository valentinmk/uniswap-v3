from eth_abi import decode
from eth_typing import ChecksumAddress
from web3.contract.contract import ContractFunction

from uniswap.EtherClient.web3_client import EtherClient
from uniswap.v3.models import Multicall2Call

from .base import BaseContract


class Multicall2(BaseContract):
    """
    Multicall2 smart contract wrapper. It is using for pack
    several read or write smart contract call in a one single call.

    Please refer official documentation (no real documentation):
    https://docs.uniswap.org/contracts/v3/reference/deployments

    Refer to source code:
    https://etherscan.io/address/0x5ba1e12693dc8f9c48aad8770482f4739beed696#code

    Parameters
    ----------
    client : EtherClient
        EtherClient Client
    address : ChecksumAddress
        Address of the Multicall2 smart contract
    abi_path : str, optional, default = "../utils/abis/multicall2.abi.json"
        Path to the ABI of the Multicall2 start contract.

    Attributes
    ----------
    client: EtherClient
    """

    def __init__(
        self,
        client: EtherClient,
        address: ChecksumAddress,
        abi_path: str = "../utils/abis/multicall2.abi.json",
    ):
        super().__init__(client.w3, address, abi_path)
        self.client = client

    def aggregate_and_call(
        self, functions: list[ContractFunction]
    ) -> list[Multicall2Call]:
        """
        Run multiple smart contract call at once

        Parameters
        ----------
        functions: list[ContractFunction]
            A list of contract call with input params.

        Returns
        -------
        calls: list[Multicall2Call]
            A list of contract call with returns.
        """
        calls: list[Multicall2Call] = [
            Multicall2Call(func_call=func) for func in functions
        ]
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
            call.returns = decode(types=list_of_typ, data=result)
            call.block_number = block_number
        return calls

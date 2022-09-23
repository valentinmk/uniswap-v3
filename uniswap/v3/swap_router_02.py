from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from uniswap.EtherClient.web3_client import EtherClient
from uniswap.v3.models import UncheckedTrade
from web3 import Web3
from web3.types import TxReceipt

from .base import BaseContract


class SwapRouter02(BaseContract):
    def __init__(
        self,
        client: EtherClient,
        w3: Web3,
        address: ChecksumAddress,
        abi_path: str = "../utils/abis/swap_router_02.abi.json",
    ):
        super().__init__(w3, address, abi_path)
        self.client = client
        self._data = None

    def _get_data(self):
        raise NotImplementedError

    @property
    def data(self):
        """Get human readable information from pool"""
        if self._data is None:
            self._data = self._get_data()
        return self._data

    def decode_multicall(self, payload):
        function_name, data = self.contract.decode_function_input(payload)
        assert (
            function_name != "<Function multicall(bytes[])>"
        ), f"Not a multicall (function_name = {function_name})"
        data = data.get("data")
        return [self.contract.decode_function_input(i) for i in data]

    def swapExactTokensForTokens(
        self,
        unchecked_trade: UncheckedTrade,
        to,
        slippage: float = 0.01,
        wait=False,
    ) -> HexBytes | TxReceipt:
        function_call = self.functions.swapExactTokensForTokens(
            unchecked_trade.raw.inputAmount,
            int(unchecked_trade.raw.outputAmount * (100 - slippage) / 100),
            unchecked_trade.raw.route,
            to,
        )
        print(function_call)
        transaction = function_call.buildTransaction(
            {
                "chainId": self.w3.eth.chain_id,
                "from": self.client.address,
                "nonce": self.w3.eth.getTransactionCount(self.client.address),
            }
        )
        private_key = self.w3.eth.account.decrypt(
            self.client._keyfile_json, self.client._wallet_pass
        )
        signed_tx = self.client.w3.eth.account.sign_transaction(
            transaction, private_key
        )
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        if wait:
            return self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_hash

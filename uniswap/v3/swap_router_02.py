from eth_typing import ChecksumAddress, HexStr
from hexbytes import HexBytes
from uniswap.EtherClient.web3_client import EtherClient
from uniswap.v3.models import UncheckedTrade
from web3.types import TxReceipt

from .base import BaseContract


class SwapRouter02(BaseContract):
    """
    SwapRouter02 contract wrapper.
    Please refer official documentation:
    https://docs.uniswap.org/contracts/v2/reference/smart-contracts/router-02

    Parameters
    ----------
    client : EtherClient
        EtherClient Client
    address : ChecksumAddress
        Address of the ERC20 token smart contract
    abi_path : str
        Path to json file with ABI of the contract. By default is
        `../utils/abis/swap_router_02.abi.json`
    """

    def __init__(
        self,
        client: EtherClient,
        address: ChecksumAddress,
        abi_path: str = "../utils/abis/swap_router_02.abi.json",
    ):
        super().__init__(client.w3, address, abi_path)
        self.client = client
        self._data = None

    def _get_data(self):
        raise NotImplementedError

    @property
    def data(self):
        """NotImplementedError"""
        if self._data is None:
            self._data = self._get_data()
        return self._data

    def decode_multicall(self, payload: HexStr) -> list:
        """
        Decode provided payload with multicall data for the array of inputs.

        Parameters
        ----------
        payload : HexStr
            Encoded smart contract call.

        Returns
        -------
        list of tuples of function objects and decoded input parameters
        """
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
        """
        Run swapExactTokensForTokens from Uniswap router 2.
        It will sell Token0 for Token1.
        Please refer official documentation:
        https://docs.uniswap.org/contracts/v2/reference/smart-contracts/router-02#swapexacttokensfortokens

        Parameters
        ----------
        unchecked_trade : UncheckedTrade
            UnChecked trade from `uni.quoter.get_trade`.
        to : ChecksumAddress
            Address of recipient wallet.
        slippage : float
            [Optional]. By default 1%. Slippage in absolute value. i.e. 50% == 0.5,
            0.1% = 0.001, 5% == 0.05
        wait : bool
            [Optional]. If true, execution will be locked until transaction not been
            verified by blockchain.
            By default is False.

        Returns
        -------
        HexBytes | TxReceipt
        """
        function_call = self.functions.swapExactTokensForTokens(
            unchecked_trade.raw.inputAmount,
            int(unchecked_trade.raw.outputAmount * (1 - slippage)),
            unchecked_trade.raw.route,
            to,
        )
        transaction = function_call.build_transaction(
            {
                "chainId": self.w3.eth.chain_id,
                "from": self.client.address,
                "nonce": self.w3.eth.get_transaction_count(self.client.address),
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

from eth_typing import ChecksumAddress
from uniswap.v3.models import Token, UncheckedTrade, UncheckedTradeRaw
from web3 import Web3

from .base import BaseContract


class Quoter(BaseContract):
    def __init__(
        self,
        w3: Web3,
        address: ChecksumAddress,
        abi_path: str = "../utils/abis/quoter.abi.json",
    ):
        super().__init__(w3, address, abi_path)
        self._data = None

    def _get_data(self):
        raise NotImplementedError

    @property
    def data(self):
        """Get human readable information from pool"""
        if self._data is None:
            self._data = self._get_data()
        return self._data

    def amount_to_wei(self, token: Token, amount):
        return int(amount * 10**token.decimals)

    def amount_from_wei(self, token: Token, amount):
        return amount / 10**token.decimals

    def _get_quote(
        self,
        token0addr: ChecksumAddress,
        token1addr: ChecksumAddress,
        fee: int,
        amount_in: int,
        trade_type: int,
    ) -> UncheckedTradeRaw:
        return UncheckedTradeRaw(
            route=[token0addr, token1addr],
            fee=fee,
            inputAmount=amount_in,
            outputAmount=self.functions.quoteExactInputSingle(
                token0addr, token1addr, fee, amount_in, trade_type
            ).call(),
            tradeType=trade_type,
        )

    def get_trade(self, token0: Token, token1: Token, fee, amount_in) -> UncheckedTrade:
        amount_in_to_wei = self.amount_to_wei(token0, amount_in)
        unchecked_trade = self._get_quote(
            token0.address, token1.address, int(fee * 10_000), amount_in_to_wei, 0
        )
        quote = self.amount_from_wei(token1, unchecked_trade.outputAmount)
        return UncheckedTrade(
            raw=unchecked_trade,
            route=[token0, token1],
            fee=fee,
            inputAmount=amount_in,
            outputAmount=quote,
            tradeType=0,
        )

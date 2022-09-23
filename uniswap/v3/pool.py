from eth_typing import ChecksumAddress
from web3 import Web3

from ..utils.erc20token import EIP20Contract
from .base import BaseContract
from .models import PoolImmutablesRaw, PoolStateRaw, PoolData, Token
from .math import from_sqrtPriceX96


class Pool(BaseContract):
    def __init__(
        self,
        client,
        w3: Web3,
        address: ChecksumAddress,
        abi_path: str = "../utils/abis/pool.abi.json",
    ):
        super().__init__(w3, address, abi_path)
        self.client = client
        self._immutables: PoolImmutablesRaw = None
        self._state: PoolStateRaw = None
        self._data: PoolData = None

    def _get_immutables(self) -> PoolImmutablesRaw:
        return PoolImmutablesRaw(
            factory=self.functions.factory().call(),
            token0=self.functions.token0().call(),
            token1=self.functions.token1().call(),
            fee=self.functions.fee().call(),
            tickSpacing=self.functions.tickSpacing().call(),
            maxLiquidityPerTick=self.functions.maxLiquidityPerTick().call(),
        )

    def _get_state(self) -> PoolStateRaw:
        (
            sqrtPriceX96,
            tick,
            observationIndex,
            observationCardinality,
            observationCardinalityNext,
            feeProtocol,
            unlocked,
        ) = self.functions.slot0().call()  # slot0
        return PoolStateRaw(
            liquidity=self.functions.liquidity().call(),
            sqrtPriceX96=sqrtPriceX96,
            tick=tick,
            observationIndex=observationIndex,
            observationCardinality=observationCardinality,
            observationCardinalityNext=observationCardinalityNext,
            feeProtocol=feeProtocol,
            unlocked=unlocked,
        )

    def _get_data(self) -> PoolData:
        return PoolData(
            immutables=self.immutables,
            state=self.state,
            token0=EIP20Contract(self.client, self.w3, self.immutables.token0).data,
            token1=EIP20Contract(self.client, self.w3, self.immutables.token1).data,
            address=self.address,
            token0Price=self._token0Price(),
            token1Price=self._token1Price(),
        )

    @property
    def immutables(self) -> PoolImmutablesRaw:
        """Get immutables"""
        if self._immutables is None:
            self._immutables = self._get_immutables()
        return self._immutables

    # XXX
    # it should be update once per block (or ~12 sec for POS and ~13 sec for POW)
    # TODO: reimplement
    @property
    def state(self) -> PoolStateRaw:
        """Get mutable parameters of a Pool"""
        if self._state is None:
            self._state = self._get_state()
        return self._state

    @property
    def data(self) -> PoolData:
        """Get human readable information from pool"""
        if self._data is None:
            self._data = self._get_data()
        return self._data

    def _token0Price(self) -> float:
        return from_sqrtPriceX96(self.state.sqrtPriceX96)

    def _token1Price(self) -> float:
        return 1 / from_sqrtPriceX96(self.state.sqrtPriceX96)

    def from_tokenPrice(self, price, token0: Token, token1: Token):
        return price / 10 ** (token1.decimals - token0.decimals)

    def token0Price(self) -> float:
        return self.data.token0Price / 10 ** (
            self.data.token1.decimals - self.data.token0.decimals
        )

    def token1Price(self) -> float:
        return self.data.token1Price / 10 ** (
            self.data.token0.decimals - self.data.token1.decimals
        )

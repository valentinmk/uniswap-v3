from dataclasses import dataclass
from eth_typing import ChecksumAddress
from uniswap.utils.consts import EXACT_INPUT, EXACT_OUTPUT


@dataclass
class Token:
    chainId: int
    decimals: int
    symbol: str
    name: str
    isNative: bool
    isToken: bool
    address: ChecksumAddress


@dataclass
class PoolImmutablesRaw:
    """Immutable Pool's data"""

    factory: ChecksumAddress
    token0: ChecksumAddress
    token1: ChecksumAddress
    fee: int
    tickSpacing: int
    maxLiquidityPerTick: int


@dataclass
class PoolStateRaw:
    """Mutable Pool's data"""

    liquidity: int
    sqrtPriceX96: int
    tick: int
    observationIndex: int
    observationCardinality: int
    observationCardinalityNext: int
    feeProtocol: int
    unlocked: bool


@dataclass
class PoolData:
    """Human-readable pool data"""

    immutables: PoolImmutablesRaw
    state: PoolStateRaw
    token0: Token
    token1: Token
    address: ChecksumAddress
    token0Price: float
    token1Price: float


@dataclass
class UncheckedTradeRaw:
    route: list[ChecksumAddress]
    fee: int
    inputAmount: int
    outputAmount: int
    tradeType: EXACT_INPUT | EXACT_OUTPUT


@dataclass
class UncheckedTrade:
    raw: UncheckedTradeRaw
    route: list[Token]
    fee: float
    inputAmount: float
    outputAmount: float
    tradeType: EXACT_INPUT | EXACT_OUTPUT

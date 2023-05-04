from dataclasses import dataclass

from eth_typing import ChecksumAddress
from web3.contract.contract import ContractFunction

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


@dataclass
class NftPositionUriData:
    name: str
    description: str
    image: str

    def __repr__(self):
        # generate very noisy output
        # for full content use implicitly __str__ method
        return (
            f"{self.__class__.__name__}(name={self.name}," "description=..., image=...)"
        )


@dataclass
class NftPositionRaw:
    token_id: int
    nonce: int
    operator: ChecksumAddress
    token0: ChecksumAddress
    token1: ChecksumAddress
    fee: int
    tickLower: int
    tickUpper: int
    liquidity: int
    feeGrowthInside0LastX128: int
    feeGrowthInside1LastX128: int
    tokensOwed0: int
    tokensOwed1: int
    token_URI_data: None


# TODO: Model too wordy, need to clean up
@dataclass
class NftPosition:
    token_id: int
    raw: NftPositionRaw
    pool: PoolData
    amount0: int = 0
    amount1: int = 0
    amount0HR: float = 0.0
    amount1HR: float = 0.0
    unclaimedfeesamount0: int = 0
    unclaimedfeesamount1: int = 0
    unclaimedfeesamount0HR: float = 0.0
    unclaimedfeesamount1HR: float = 0.0
    lower_price: float = 0.0
    upper_price: float = 0.0
    lower_price_inverse: float = 0.0
    upper_price_inverse: float = 0.0
    token0: Token = None
    token1: Token = None
    fee: float = 0.0


@dataclass
class UncheckedNftPositionRaw:
    pool: PoolData
    current_tick: int
    current_price_x96: int
    lower_tick: int
    upper_tick: int
    amount0: int
    amount1: int


@dataclass
class UncheckedNftPosition:
    raw: UncheckedNftPositionRaw
    lower_price: float = 0.0
    upper_price: float = 0.0
    amount0: int = 0
    amount1: int = 0
    amount0HR: float = 0.0
    amount1HR: float = 0.0
    token0: Token = None
    token1: Token = None
    fee: float = 0.0
    # adjusted data (by tickSpacing)
    adj_amount0: int = 0
    adj_amount1: int = 0
    adj_amount0HR: float = 0.0
    adj_amount1HR: float = 0.0
    adj_lower_price: float = 0.0
    adj_upper_price: float = 0.0


@dataclass
class Multicall2Call:
    """This is a helper dataclass for the Multicall2."""

    func_call: ContractFunction
    name: str = ""
    returns: list[tuple] = None
    outputs: list[dict] = None
    block_number: int = 0

from ..v3.models import Token


ROPSTEN_USDC = ROPSTEN_USDC_TOKEN = Token(
    chainId=3,
    decimals=6,
    symbol="USDC",
    name="USD Coin",
    isNative=False,
    isToken=True,
    address="0x07865c6E87B9F70255377e024ace6630C1Eaa37F",
)
ROPSTEN_WETH = ROPSTEN_USDC_TOKEN = Token(
    chainId=3,
    decimals=18,
    symbol="WETH",
    name="Wrapped Ether",
    isNative=False,
    isToken=True,
    address="0xc778417E063141139Fce010982780140Aa0cD5Ab",
)
ROPSTEN_AAVE = ROPSTEN_AAVE_TOKEN = Token(
    chainId=3,
    decimals=18,
    symbol="AAVE",
    name="AAVE",
    isNative=False,
    isToken=True,
    address="0xa17669420eD99FAc51308567B08B7BaC86837BAf",
)

ROPSTEN_COMP = ROPSTEN_COMP_TOKEN = Token(
    chainId=3,
    decimals=18,
    symbol="COMP",
    name="Compound",
    isNative=False,
    isToken=True,
    address="0xf76D4a441E4ba86A923ce32B89AFF89dBccAA075",
)

ROPSTEN_UNI = ROPSTEN_UNI_TOKEN = Token(
    chainId=3,
    decimals=18,
    symbol="UNI",
    name="Uniswap",
    isNative=False,
    isToken=True,
    address="0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
)

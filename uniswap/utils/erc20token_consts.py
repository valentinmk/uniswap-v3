from ..v3.models import Token


GOERLI_USDC_TOKEN = Token(
    chainId=5,
    decimals=6,
    symbol="USDC",
    name="USD Coin",
    isNative=False,
    isToken=True,
    address="0x07865c6E87B9F70255377e024ace6630C1Eaa37F",
)
GOERLI_DAI_TOKEN = Token(
    chainId=5,
    decimals=18,
    symbol="DAI",
    name="Dai Stablecoin",
    isNative=False,
    isToken=True,
    address="0x11fE4B6AE13d2a6055C8D9cF65c55bac32B5d844",
)
GOERLI_WETH_TOKEN = Token(
    chainId=5,
    decimals=18,
    symbol="WETH",
    name="Wrapped Ether",
    isNative=False,
    isToken=True,
    address="0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6",
)
GOERLI_AAVE_TOKEN = Token(
    chainId=5,
    decimals=18,
    symbol="AAVE",
    name="AAVE",
    isNative=False,
    isToken=True,
    address="0x63242B9Bd3C22f18706d5c4E627B4735973f1f07",
)

GOERLI_COMP_TOKEN = Token(
    chainId=5,
    decimals=18,
    symbol="COMP",
    name="Compound",
    isNative=False,
    isToken=True,
    address="0x3587b2F7E0E2D6166d6C14230e7Fe160252B0ba4",
)

GOERLI_UNI_TOKEN = Token(
    chainId=5,
    decimals=18,
    symbol="UNI",
    name="Uniswap",
    isNative=False,
    isToken=True,
    address="0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
)

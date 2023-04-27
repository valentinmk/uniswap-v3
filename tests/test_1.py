import os
import pytest
from uniswap.EtherClient.web3_client import EtherClient
from uniswap.utils.consts import ERC20_TOKENS, GOERLI
from uniswap.utils.erc20token import EIP20Contract
from uniswap.v3.main import UniswapV3


@pytest.mark.release
@pytest.mark.devel
def test_client_invoke():
    client = EtherClient(http_url=os.environ.get("ETH_PROVIDER_URL"))
    assert client.url == os.environ.get("ETH_PROVIDER_URL")
    assert client.address is None


@pytest.mark.release
@pytest.mark.devel
def test_client():
    client = EtherClient(http_url=os.environ.get("ETH_PROVIDER_URL"))
    balance = client.w3.eth.get_balance("0x0000000000000000000000000000000000000000")
    assert (
        type(balance) is int
        and balance > 0
        and balance > int(11400.554402868460904505 * 10**18)
    )


@pytest.mark.release
@pytest.mark.devel
@pytest.mark.asyncio
async def test_async_client():
    client = EtherClient(http_url=os.environ.get("ETH_PROVIDER_URL"), http_async=True)
    balance = await client.w3.eth.get_balance(
        "0x0000000000000000000000000000000000000000"
    )
    assert type(balance) is int
    assert balance > 0
    assert balance > int(11400.554402868460904505 * 10**18)


@pytest.mark.release
@pytest.mark.devel
def test_ws_client():
    client = EtherClient(ws_url=os.environ.get("ETH_PROVIDER_WS"))
    balance = client.w3.eth.get_balance("0x0000000000000000000000000000000000000000")
    assert (
        type(balance) is int
        and balance > 0
        and balance > int(11400.554402868460904505 * 10**18)
    )


@pytest.mark.release
@pytest.mark.devel
def test_none_client():
    client = EtherClient()
    with pytest.raises(BaseException) as exc_info:
        client.w3
    assert str(exc_info.value) == "unable to define Ether Provider"


@pytest.mark.release
@pytest.mark.devel
def test_uniswap(eth_client: EtherClient):
    uni = UniswapV3(eth_client)
    assert uni.client is not None


testdata_erc20 = [
    (ERC20_TOKENS[GOERLI]["USDC"], 6, "USD Coin"),
    (ERC20_TOKENS[GOERLI]["DAI"], 18, "Dai Stablecoin"),
]


@pytest.mark.release
@pytest.mark.devel
@pytest.mark.parametrize("address, decimal, name", testdata_erc20)
def test_EIP20Contract(eth_client: EtherClient, address, decimal, name):
    usdc = EIP20Contract(eth_client, address)
    assert usdc.data.decimals == decimal
    assert usdc.data.name == name


testdata_pools = [
    (
        ERC20_TOKENS[GOERLI]["WETH"],
        ERC20_TOKENS[GOERLI]["USDC"],
        500,
        "0xfAe941346Ac34908b8D7d000f86056A18049146E",
    ),
    (
        ERC20_TOKENS[GOERLI]["WETH"],
        ERC20_TOKENS[GOERLI]["DAI"],
        500,
        "0x6D148b26d4BA7365989702E8af2449DDDd2a77A0",
    ),
]


@pytest.mark.release
@pytest.mark.devel
@pytest.mark.parametrize("token1, token2, fee, address", testdata_pools)
def test_uni_pool_invoke(
    uni: UniswapV3,
    token1,
    token2,
    fee,
    address,
):
    pool_address = uni.factory.functions.getPool(token1, token2, fee).call()
    assert pool_address == address


@pytest.mark.release
@pytest.mark.devel
@pytest.mark.parametrize("token1, token2, fee, address", testdata_pools)
def test_uni_pool_data(
    uni: UniswapV3,
    token1,
    token2,
    fee,
    address,
):
    pool = uni.get_pool(token1, token2, fee)
    im_data = pool.immutables
    state_data = pool._get_state()
    data = pool.data
    # -- im_data --
    assert type(im_data.factory) is str and im_data
    assert type(im_data.token0) is str and im_data.token0 in (token1, token2)
    assert type(im_data.token1) is str and im_data.token0 in (token1, token2)
    assert type(im_data.fee) is int and im_data.fee == fee
    assert type(im_data.tickSpacing) is int and im_data.tickSpacing > 0
    assert type(im_data.maxLiquidityPerTick) is int and im_data.maxLiquidityPerTick > 0
    # -- state_data --
    assert type(state_data.liquidity) is int and state_data.liquidity >= 0
    assert type(state_data.sqrtPriceX96) is int and state_data.sqrtPriceX96 > 0
    assert type(state_data.tick) is int
    assert type(state_data.observationIndex) is int
    assert type(state_data.observationCardinality) is int
    assert type(state_data.observationCardinalityNext) is int
    assert type(state_data.feeProtocol) is int
    assert type(state_data.unlocked) is bool
    # -- data --
    assert data.immutables == im_data
    assert data.state == state_data

    price0 = pool.token0Price()
    price1 = pool.token1Price()
    print(price0)
    print(price1)
    assert price0 == 1 / price1

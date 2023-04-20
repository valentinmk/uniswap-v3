import os
import pytest
from uniswap.EtherClient.web3_client import EtherClient
from uniswap.utils.consts import ERC20_TOKENS, GOERLI
from uniswap.utils.erc20token import EIP20Contract
from uniswap.v3.main import UniswapV3


def test_client_invoke():
    client = EtherClient(http_url=os.environ.get("ETH_PROVIDER_URL"))
    assert client.url == os.environ.get("ETH_PROVIDER_URL")
    assert client.address is None


def test_client():
    client = EtherClient(http_url=os.environ.get("ETH_PROVIDER_URL"))
    balance = client.w3.eth.get_balance("0x0000000000000000000000000000000000000000")
    assert (
        type(balance) is int
        and balance > 0
        and balance > int(11400.554402868460904505 * 10**18)
    )


@pytest.mark.asyncio
async def test_async_client():
    client = EtherClient(http_url=os.environ.get("ETH_PROVIDER_URL"), http_async=True)
    balance = await client.w3.eth.get_balance(
        "0x0000000000000000000000000000000000000000"
    )
    assert type(balance) is int
    assert balance > 0
    assert balance > int(11400.554402868460904505 * 10**18)


def test_ws_client():
    client = EtherClient(ws_url=os.environ.get("ETH_PROVIDER_WS"))
    balance = client.w3.eth.get_balance("0x0000000000000000000000000000000000000000")
    assert (
        type(balance) is int
        and balance > 0
        and balance > int(11400.554402868460904505 * 10**18)
    )


def test_none_client():
    client = EtherClient()
    with pytest.raises(BaseException) as exc_info:
        client.w3
    assert str(exc_info.value) == "unable to define Ether Provider"


def test_uniswap(eth_client):
    uni = UniswapV3(eth_client)
    assert uni.client is not None


def test_EIP20Contract(eth_client):
    usdc = EIP20Contract(eth_client, eth_client.w3, ERC20_TOKENS[GOERLI]["USDC"])
    assert usdc.data.decimals == 6
    assert usdc.data.name == "USD Coin"


def test_uni_factory(uni, weth, dai):
    pool_address = uni.factory.functions.getPool(weth.address, dai.address, 500).call()
    assert pool_address == "0x6D148b26d4BA7365989702E8af2449DDDd2a77A0"


def test_draft():
    # TODO
    # Work in progress. It's a mess for now.
    # provide complete integration and unit tests.
    # client = EtherClient(http_url=os.environ.get("ETH_PROVIDER_URL"))
    client = EtherClient(ws_url=os.environ.get("ETH_PROVIDER_WS"))
    print(client.w3.eth.block_number)

    uni = UniswapV3(client)
    usdc = EIP20Contract(client, client.w3, ERC20_TOKENS[GOERLI]["USDC"])
    dai = EIP20Contract(client, client.w3, ERC20_TOKENS[GOERLI]["DAI"])
    weth = EIP20Contract(client, client.w3, ERC20_TOKENS[GOERLI]["WETH"])
    print(usdc.data)
    print(dai.data)
    print(weth.data)
    # print(uni.factory.get_functions())

    # print(client.w3.eth.chain_id)
    # print(ERC20_TOKENS[ROPSTEN]["USDC"], ERC20_TOKENS[ROPSTEN]["WETH"], 500)
    # print(uni.factory.abi)
    print(uni.factory.functions.getPool(usdc.address, weth.address, 500).call())
    # print(uni.get_pool(
    #   ERC20_TOKENS[ROPSTEN]["USDC"], ERC20_TOKENS[ROPSTEN]["WETH"], 500
    # ))
    pool = uni.get_pool(usdc.address, weth.address, 500)
    print(pool)
    print(pool.address)
    print(pool.get_functions())
    print(pool.functions.maxLiquidityPerTick().call())
    # print(pool._get_immutables())
    print(pool.immutables)
    print(pool._get_state())

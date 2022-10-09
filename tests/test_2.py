import os
from uniswap.EtherClient import web3_client
from uniswap.v3.main import UniswapV3
from uniswap.utils.erc20token import EIP20Contract
from uniswap.utils.consts import ERC20_TOKENS, GOERLI
from uniswap.v3 import math
from uniswap.utils.erc20token_consts import GOERLI_USDC_TOKEN, GOERLI_WETH_TOKEN


def test_draft():
    # TODO
    # Work in progress. It's a mess for now.
    # provide complete integration and unit tests.
    client = web3_client.EtherClient(http_url=os.environ.get("ETH_PROVIDER_URL"))
    # client.w3
    print(client.w3.eth.block_number)

    uni = UniswapV3(client)
    usdc = EIP20Contract(client, client.w3, ERC20_TOKENS[GOERLI]["USDC"])
    weth = EIP20Contract(client, client.w3, ERC20_TOKENS[GOERLI]["WETH"])
    print(usdc.data)
    print(weth.data)
    print(GOERLI_USDC_TOKEN)
    print(GOERLI_WETH_TOKEN)

    # print(uni.factory.get_functions())

    # print(client.w3.eth.chain_id)
    # print(ERC20_TOKENS[ROPSTEN]["USDC"], ERC20_TOKENS[ROPSTEN]["WETH"], 500)
    # print(uni.factory.abi)
    print(
        uni.factory.functions.getPool(
            GOERLI_USDC_TOKEN.address, GOERLI_WETH_TOKEN.address, 500
        ).call()
    )
    # print(uni.get_pool(
    #   ERC20_TOKENS[ROPSTEN]["USDC"],
    #   ERC20_TOKENS[ROPSTEN]["WETH"],
    #   500))
    pool = uni.get_pool(GOERLI_USDC_TOKEN.address, GOERLI_WETH_TOKEN.address, 500)
    print(pool)
    print(pool.address)
    print(pool.get_functions())
    print(pool.functions.maxLiquidityPerTick().call())
    # print(pool._get_immutables())
    print(pool.immutables)
    print(pool._get_state())
    price = math.from_sqrtPriceX96(pool.state.sqrtPriceX96) / 10 ** (
        GOERLI_WETH_TOKEN.decimals - GOERLI_USDC_TOKEN.decimals
    )
    print(
        GOERLI_USDC_TOKEN.symbol,
        GOERLI_WETH_TOKEN.symbol,
        f"{price:.8f}",
    )
    price = 1 / (
        math.from_sqrtPriceX96(pool.state.sqrtPriceX96)
        / 10 ** (GOERLI_WETH_TOKEN.decimals - GOERLI_USDC_TOKEN.decimals)
    )
    print(
        GOERLI_WETH_TOKEN.symbol,
        GOERLI_USDC_TOKEN.symbol,
        f"{price:.8f}",
    )
    # print(
    #     math.from_sqrtPriceX96(pool.state.liquidity)
    #     * 10 ** (ROPSTEN_WETH.decimals - ROPSTEN_USDC.decimals)
    # )

    print("*" * 100)
    print(pool.data)
    print("*" * 100)
    print(pool.token0Price())
    print(pool.token1Price())
    # print(pool._token0Price())
    # print(pool._token1Price())
    # print(pool.from_tokenPrice(pool._token0Price(), 6, 18))
    # print(pool.from_tokenPrice(pool._token1Price(), 18, 6))
    # print(
    #     weth.data.symbol,
    #     usdc.data.symbol,
    #     1 / math.from_sqrtPriceX96(pool.state.sqrtPriceX96),
    # )

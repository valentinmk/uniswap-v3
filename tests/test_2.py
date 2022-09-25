import os
from uniswap.EtherClient import web3_client
from uniswap.v3.main import UniswapV3
from uniswap.utils.erc20token import EIP20Contract
from uniswap.utils.consts import ERC20_TOKENS, ROPSTEN
from uniswap.v3 import math
from uniswap.utils.erc20token_consts import ROPSTEN_USDC, ROPSTEN_WETH


def test_draft():
    # TODO
    # Work in progress. It's a mess for now.
    # provide complete integration and unit tests.
    client = web3_client.EtherClient(http_url=os.environ.get("ETH_PROVIDER_URL"))
    # client.w3
    print(client.w3.eth.block_number)

    uni = UniswapV3(client)
    usdc = EIP20Contract(client, client.w3, ERC20_TOKENS[ROPSTEN]["USDC"])
    weth = EIP20Contract(client, client.w3, ERC20_TOKENS[ROPSTEN]["WETH"])
    print(usdc.data)
    print(weth.data)
    print(ROPSTEN_USDC)
    print(ROPSTEN_WETH)

    # print(uni.factory.get_functions())

    # print(client.w3.eth.chain_id)
    # print(ERC20_TOKENS[ROPSTEN]["USDC"], ERC20_TOKENS[ROPSTEN]["WETH"], 500)
    # print(uni.factory.abi)
    print(
        uni.factory.functions.getPool(
            ROPSTEN_USDC.address, ROPSTEN_WETH.address, 500
        ).call()
    )
    # print(uni.get_pool(
    #   ERC20_TOKENS[ROPSTEN]["USDC"],
    #   ERC20_TOKENS[ROPSTEN]["WETH"],
    #   500))
    pool = uni.get_pool(ROPSTEN_USDC.address, ROPSTEN_WETH.address, 500)
    print(pool)
    print(pool.address)
    print(pool.get_functions())
    print(pool.functions.maxLiquidityPerTick().call())
    # print(pool._get_immutables())
    print(pool.immutables)
    print(pool._get_state())
    price = math.from_sqrtPriceX96(pool.state.sqrtPriceX96) / 10 ** (
        ROPSTEN_WETH.decimals - ROPSTEN_USDC.decimals
    )
    print(
        ROPSTEN_USDC.symbol,
        ROPSTEN_WETH.symbol,
        f"{price:.8f}",
    )
    price = 1 / (
        math.from_sqrtPriceX96(pool.state.sqrtPriceX96)
        / 10 ** (ROPSTEN_WETH.decimals - ROPSTEN_USDC.decimals)
    )
    print(
        ROPSTEN_WETH.symbol,
        ROPSTEN_USDC.symbol,
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

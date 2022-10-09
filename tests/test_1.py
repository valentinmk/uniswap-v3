import os
from uniswap.EtherClient import web3_client
from uniswap.utils.consts import ERC20_TOKENS, GOERLI
from uniswap.utils.erc20token import EIP20Contract
from uniswap.v3.main import UniswapV3


def test_draft():
    # TODO
    # Work in progress. It's a mess for now.
    # provide complete integration and unit tests.
    client = web3_client.EtherClient(http_url=os.environ.get("ETH_PROVIDER_URL"))
    print(client.w3.eth.block_number)

    uni = UniswapV3(client)
    usdc = EIP20Contract(client, client.w3, ERC20_TOKENS[GOERLI]["USDC"])
    weth = EIP20Contract(client, client.w3, ERC20_TOKENS[GOERLI]["WETH"])
    print(usdc.data)
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

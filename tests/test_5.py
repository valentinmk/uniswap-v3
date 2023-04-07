import os
import json
from eth_abi import decode
from web3 import Web3
from uniswap.EtherClient import web3_client
from uniswap.v3.main import UniswapV3

from uniswap.utils.erc20token import EIP20Contract
from uniswap.utils.consts import ERC20_TOKENS


def test_draft():
    # TODO
    # Work in progress. It's a mess for now.
    # provide complete integration and unit tests.
    MY_ADDRESS = Web3.to_checksum_address("0x997d4c6A7cA5d524babDf1b205351f6FB623b5E7")

    ETH_HTTP_URL = os.environ.get("ETH_PROVIDER_URL")
    ETH_WALLET_PASS = os.environ.get("ETH_WALLET_PASS")
    ETH_WALLET_JSON_PATH = os.environ.get("ETH_WALLET_JSON_PATH")
    with open(ETH_WALLET_JSON_PATH) as keyfile:
        ETH_WALLET_JSON = keyfile.read()
    eth_client = web3_client.EtherClient(
        http_url=ETH_HTTP_URL,
        my_address=MY_ADDRESS,
        my_wallet_pass=ETH_WALLET_PASS,
        my_keyfile_json=ETH_WALLET_JSON,
    )
    print(eth_client.w3.eth.block_number)
    uni = UniswapV3(eth_client)

    usdc = EIP20Contract(eth_client, eth_client.w3, ERC20_TOKENS[5]["USDC"])
    weth = EIP20Contract(eth_client, eth_client.w3, ERC20_TOKENS[5]["WETH"])
    print(usdc)
    print(usdc.data)
    # print(uni.swap_router_02.address)
    # print(usdc.allowance(uni.swap_router_02.address))

    print(uni.nft_position_manager.address)
    print(uni.nft_position_manager.get_functions())

    ###
    print(usdc.get_functions())
    print(usdc.functions.name().abi.get("outputs"))
    print(usdc.functions.decimals()._encode_transaction_data())
    print(usdc.functions.symbol())
    usdc_encoded_funcs = (
        usdc.functions.name()._encode_transaction_data(),
        usdc.functions.decimals()._encode_transaction_data(),
        usdc.functions.symbol()._encode_transaction_data(),
    )
    usdc_outputs = (
        usdc.functions.name().abi.get("outputs"),
        usdc.functions.decimals().abi.get("outputs"),
        usdc.functions.symbol().abi.get("outputs"),
    )
    weth_encoded_funcs = (
        weth.functions.name()._encode_transaction_data(),
        weth.functions.decimals()._encode_transaction_data(),
        weth.functions.symbol()._encode_transaction_data(),
    )
    weth_outputs = (
        weth.functions.name().abi.get("outputs"),
        weth.functions.decimals().abi.get("outputs"),
        weth.functions.symbol().abi.get("outputs"),
    )
    usdc_encoded_funcs += weth_encoded_funcs
    usdc_outputs += weth_outputs
    print(usdc_encoded_funcs)
    print(usdc_outputs)
    print("*" * 100)
    path = "multicall2.abi.json"
    abi_file = open(f"{os.path.dirname(__file__)}/../uniswap/utils/abis/{path}")
    # print(abi_file)
    abi = json.load(abi_file)
    multicall2 = eth_client.w3.eth.contract(
        address="0x5BA1e12693Dc8F9c48aAD8770482f4739bEeD696", abi=abi
    )
    print(
        multicall2.functions.aggregate(
            [{"target": usdc.address, "callData": i} for i in usdc_encoded_funcs]
        )
    )
    output = multicall2.functions.aggregate(
        [{"target": usdc.address, "callData": i} for i in usdc_encoded_funcs]
    ).call()
    [print(o) for o in output[1]]
    for i, o in enumerate(output[1]):
        print(usdc_outputs[i])
        list_of_typ = [j["type"] for j in usdc_outputs[i]]
        print(list_of_typ)
        print(decode(types=list_of_typ, data=o))

    print("_" * 100)
    print(uni.multicall2.get_functions())
    [
        print(i)
        for i in uni.multicall2.aggregate_and_call(
            [
                usdc.functions.name(),
                usdc.functions.decimals(),
                usdc.functions.symbol(),
                usdc.functions.totalSupply(),
                weth.functions.name(),
                weth.functions.decimals(),
                weth.functions.symbol(),
                weth.functions.totalSupply(),
            ]
        )
    ]
    pool_address_raw = uni.multicall2.aggregate_and_call(
        [uni.factory.functions.getPool(usdc.address, weth.address, 500)]
    )
    print(pool_address_raw[0].returns[0])
    pool = uni.get_pool(usdc.address, weth.address, 500)
    slot0_0 = pool.functions.slot0().call()
    print(slot0_0)
    slot0_raw = uni.multicall2.aggregate_and_call([pool.functions.slot0()])
    slot0_1 = slot0_raw[0].returns
    print(slot0_1)
    print(tuple(slot0_0) == tuple(slot0_1))
    assert tuple(slot0_0) == tuple(slot0_1)

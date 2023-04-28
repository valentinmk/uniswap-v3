import os

import pytest
from web3 import Web3
from uniswap.EtherClient.web3_client import EtherClient
from uniswap.EtherClient import web3_client

from uniswap.v3.main import UniswapV3
from uniswap.v3.models import Token
from uniswap.utils.erc20token import EIP20Contract
from uniswap.utils.erc20token_consts import (
    GOERLI_DAI_TOKEN,
    GOERLI_WETH_TOKEN,
    GOERLI_UNI_TOKEN,
)


@pytest.fixture(scope="module")
def eth_client():
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
    return eth_client


@pytest.fixture(scope="module")
def uni(eth_client) -> UniswapV3:
    return UniswapV3(eth_client)


@pytest.fixture(scope="module")
def weth() -> Token:
    return GOERLI_WETH_TOKEN


@pytest.fixture(scope="module")
def dai() -> Token:
    return GOERLI_DAI_TOKEN


@pytest.fixture(scope="module")
def uni_token() -> Token:
    return GOERLI_UNI_TOKEN


@pytest.fixture(scope="module")
def dai_contract(eth_client: EtherClient, dai) -> EIP20Contract:
    contract = EIP20Contract(eth_client, dai.address)
    return contract


@pytest.fixture(scope="module")
def weth_contract(eth_client: EtherClient, weth) -> EIP20Contract:
    contract = EIP20Contract(eth_client, weth.address)
    return contract


@pytest.fixture(scope="module")
def pool_dai_weth(uni: UniswapV3, dai: Token, weth: Token):
    return uni.get_pool(dai.address, weth.address, fee=500)
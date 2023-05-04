import pytest

from uniswap.utils.erc20token import EIP20Contract
from uniswap.v3.main import UniswapV3
from uniswap.v3.models import Token, Multicall2Call


@pytest.mark.release
@pytest.mark.devel
def test_multicall_aggregate_and_call(uni: UniswapV3, dai_contract: EIP20Contract):
    dai_encoded_funcs = (
        dai_contract.functions.decimals(),
        dai_contract.functions.symbol(),
        dai_contract.functions.name(),
    )
    result = uni.multicall2.aggregate_and_call(dai_encoded_funcs)
    assert type(result[0]) is Multicall2Call
    assert result[0].returns[0] == 18
    assert result[1].returns[0] == "DAI"
    assert result[2].returns[0] == "Dai Stablecoin"


@pytest.mark.release
@pytest.mark.devel
def test_multicall_fast(uni: UniswapV3, dai_contract: EIP20Contract, dai: Token):
    dai_encoded_funcs = (
        dai_contract.functions.decimals(),
        dai_contract.functions.symbol(),
        dai_contract.functions.name(),
    )
    result = uni.multicall2.aggregate_and_call(dai_encoded_funcs)
    fast_token = Token(
        chainId=uni.w3.eth.chain_id,
        decimals=result[0].returns[0],
        symbol=result[1].returns[0],
        name=result[2].returns[0],
        isNative=False,
        isToken=True,
        address=dai_contract.address,
    )
    assert fast_token == dai


@pytest.mark.release
@pytest.mark.devel
def test_multicall_fast_timeit(uni: UniswapV3, dai_contract: EIP20Contract, dai: Token):
    import timeit

    def create_fast():
        dai_encoded_funcs = (
            dai_contract.functions.decimals(),
            dai_contract.functions.symbol(),
            dai_contract.functions.name(),
        )
        result = uni.multicall2.aggregate_and_call(dai_encoded_funcs)
        fast_token = Token(
            chainId=uni.w3.eth.chain_id,
            decimals=result[0].returns[0],
            symbol=result[1].returns[0],
            name=result[2].returns[0],
            isNative=False,
            isToken=True,
            address=dai_contract.address,
        )
        return fast_token

    def create():
        token = EIP20Contract(uni.client, dai.address).data
        return token

    time_create = timeit.timeit(create, number=1, globals=globals())
    time_create_fast = timeit.timeit(create_fast, number=1, globals=globals())
    assert time_create > time_create_fast
    assert create_fast() == create()

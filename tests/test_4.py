import pytest
from web3.exceptions import ContractLogicError

from uniswap.v3.main import UniswapV3
from uniswap.v3.models import Token


@pytest.mark.release
@pytest.mark.devel
def test_test(uni: UniswapV3):
    npm_address = uni.nft_position_manager.address
    assert npm_address == "0xC36442b4a4522E871399CD717aBDD847Ab11FE88"
    function_list = [
        "burn",
        "collect",
        "decreaseLiquidity",
        "increaseLiquidity",
        "mint",
    ]
    npm_functions = uni.nft_position_manager.get_functions()
    assert all([i in npm_functions for i in function_list])
    n_of_nft_possiotions = uni.nft_position_manager._fetch_balance_of()
    assert type(n_of_nft_possiotions) is int and n_of_nft_possiotions >= 0


@pytest.mark.release
@pytest.mark.devel
def test_position_get(uni: UniswapV3):
    if uni.nft_position_manager._fetch_balance_of() > 0:
        first_nft_id = uni.nft_position_manager._fetch_token_owner_by_index(0)
        assert first_nft_id > 0 and type(first_nft_id) is int
    else:
        pass
    with pytest.raises(ContractLogicError) as exc:
        first_nft_id = uni.nft_position_manager._fetch_token_owner_by_index(
            index=0, address="0x0000000000000000000000000000000000000000"
        )
    assert str(exc.value) == "execution reverted: EnumerableSet: index out of bounds"


@pytest.mark.release
@pytest.mark.devel
def test_position_token_uri(uni: UniswapV3):
    token_uri_info = uni.nft_position_manager._fetch_token_uri(21794)
    assert token_uri_info.name.startswith("Uniswap")
    assert token_uri_info.description
    assert token_uri_info.image


@pytest.mark.release
@pytest.mark.devel
def test_position_info(uni: UniswapV3):
    token_raw_info = uni.nft_position_manager._fetch_position_info(21794)
    assert token_raw_info.token_id
    assert token_raw_info.token0
    assert token_raw_info.token1
    assert token_raw_info.fee
    assert token_raw_info.tickLower
    assert token_raw_info.tickUpper
    assert token_raw_info.liquidity
    assert token_raw_info.token_URI_data


@pytest.mark.release
@pytest.mark.devel
def test_position__get_position(uni: UniswapV3):
    token_raw_info = uni.nft_position_manager._fetch_position_info(21794)
    pool = uni.get_pool(
        token_raw_info.token0, token_raw_info.token1, token_raw_info.fee
    )
    position = uni.nft_position_manager._get_position(
        token_raw_info.token_id, position_raw=token_raw_info, pool=pool
    )
    assert position.amount0HR
    assert position.amount1HR


@pytest.mark.release
@pytest.mark.devel
def test_position__get_mint_tx(uni: UniswapV3, weth: Token, dai: Token):
    # due to price changing it is not possible to provide some
    # some fixed data to test mint function
    # so i am using uni.nft_position_manager.create_position to generate
    # test data
    pool = uni.get_pool(
        token0=dai.address,
        token1=weth.address,
        fee=500,
    )
    uc_position = uni.nft_position_manager.create_position(
        pool_data=pool.data,
        current_price=pool.data.token0Price,
        lower_price=pool.data.token0Price * 0.9,
        upper_price=pool.data.token0Price * 1.9,
        amount0=100,
    )
    tx_params = uni.nft_position_manager._get_mint_tx(
        token0=dai.address,
        token1=weth.address,
        fee=500,
        tick_lower=pool.state.tick - pool.data.immutables.tickSpacing,
        tick_upper=pool.state.tick + pool.data.immutables.tickSpacing,
        amount0=uc_position.adj_amount0,
        amount1=uc_position.adj_amount1,
        amount0_min=0,
        amount1_min=0,
    )
    assert tx_params.get("value") == 0


@pytest.mark.release
@pytest.mark.devel
def test_position__get_increase_tx(uni: UniswapV3, weth: Token, uni_token: Token):
    # using pre-created liquidity position
    # with a lower/upper price pre-setted to be "in range"
    # could fail due to create_position currently not handle
    # a situation of one-token liquidity calculation
    pool = uni.get_pool(
        token0=uni_token.address,
        token1=weth.address,
        fee=500,
    )
    uc_position = uni.nft_position_manager.create_position(
        pool_data=pool.data,
        current_price=pool.data.token0Price,
        lower_price=pool.data.token0Price * 0.9,
        upper_price=pool.data.token0Price * 1.9,
        amount0=0.01,
    )
    tx_params = uni.nft_position_manager._get_increase_liquidity_tx(
        token_id=65590,
        amount0=uc_position.adj_amount0,
        amount1=uc_position.adj_amount1,
        amount0_min=0,
        amount1_min=0,
    )
    assert tx_params.get("value") == 0


@pytest.mark.release
@pytest.mark.devel
def test_position__get_decrease_tx(uni: UniswapV3, weth: Token, uni_token: Token):
    tx_params = uni.nft_position_manager._get_decrease_liquidity_tx(
        token_id=65590,
        liquidity=10,
        amount0_min=0,
        amount1_min=0,
    )
    assert tx_params.get("value") == 0


@pytest.mark.release
@pytest.mark.devel
def test_position__get_collect_tx(uni: UniswapV3, weth: Token, uni_token: Token):
    tx_params = uni.nft_position_manager._get_collect_tx(token_id=65590)
    assert tx_params.get("value") == 0

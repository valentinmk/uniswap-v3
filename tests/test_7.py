import pytest
from .helpers.models import LiquidityPosition

from uniswap.v3.main import UniswapV3
from uniswap.v3.pool import Pool
from uniswap.v3.models import Token, PoolData, PoolImmutablesRaw, PoolStateRaw
from uniswap.v3.math import (
    from_sqrtPriceX96,
    get_sqrt_ratio_at_tick,
    get_amount0_from_price_range,
    get_amount1_from_price_range,
    get_amount0_from_tick_range,
    get_amount1_from_tick_range,
)


@pytest.mark.release
@pytest.mark.devel
def test_print_mint_sc_call(uni: UniswapV3):
    hex_data = "0x8831645600000000000000000000000011fe4b6ae13d2a6055c8d9cf65c55bac32b5d844000000000000000000000000b4fbf271143f4fbf7b91a5ded31805e42b2208d600000000000000000000000000000000000000000000000000000000000001f4fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe9350fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe93a00000000000000000000000000000000000000000000000008ac7230489e7fc250000000000000000000000000000000000000000000000000002834e49228be700000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000997d4c6a7ca5d524babdf1b205351f6fb623b5e700000000000000000000000000000000000000000000000000000000642a8f9c"  # noqa
    call_data = uni.nft_position_manager.contract.decode_function_input(hex_data)
    assert call_data[0].fn_name == "mint"


test_position = LiquidityPosition(
    # Pair of Tokens with same decimals
    # Test with predefined data
    # Example pool state
    current_price_x96=745530830026153871741189246,
    current_tick=-93325,
    # Example position input params
    current_price=0.0000885466,
    lower_price=0.000088233,
    upper_price=0.000088941,
    lower_tick=-93360,
    upper_tick=-93280,
    amount0=9999999999999999013,
    amount1=707322211109863,
    liquidity=0,
    amount0HR=10,
    amount1HR=0.000707322,
)
# test pool data (it constantly changing in the testnet)
# for testing need we are fixed some state
test_pool_data = PoolData(
    immutables=PoolImmutablesRaw(
        factory="0x1F98431c8aD98523631AE4a59f267346ea31F984",
        token0="0x11fE4B6AE13d2a6055C8D9cF65c55bac32B5d844",
        token1="0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6",
        fee=500,
        tickSpacing=10,
        maxLiquidityPerTick=1917569901783203986719870431555990,
    ),
    state=PoolStateRaw(
        liquidity=813638841465295002128,
        sqrtPriceX96=745530830026153871741189246,
        tick=-93325,
        observationIndex=334,
        observationCardinality=500,
        observationCardinalityNext=500,
        feeProtocol=0,
        unlocked=True,
    ),
    token0=Token(
        chainId=5,
        decimals=18,
        symbol="DAI",
        name="Dai Stablecoin",
        isNative=False,
        isToken=True,
        address="0x11fE4B6AE13d2a6055C8D9cF65c55bac32B5d844",
    ),
    token1=Token(
        chainId=5,
        decimals=18,
        symbol="WETH",
        name="Wrapped Ether",
        isNative=False,
        isToken=True,
        address="0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6",
    ),
    address="0x6D148b26d4BA7365989702E8af2449DDDd2a77A0",
    token0Price=8.854663217996205e-05,
    token1Price=11293.48429613451,
)

test_data = [(test_position, test_pool_data)]


@pytest.mark.release
@pytest.mark.devel
@pytest.mark.parametrize("position, pool", test_data)
def test_synth_math_from_sqrtPriceX96(position: LiquidityPosition, pool: PoolData):
    assert position.current_price == round(
        from_sqrtPriceX96(position.current_price_x96), 10
    )
    assert test_position.current_price != from_sqrtPriceX96(
        get_sqrt_ratio_at_tick(position.current_tick)
    )
    assert position.current_price_x96 != get_sqrt_ratio_at_tick(position.current_tick)
    assert 5000 == from_sqrtPriceX96(5602277097478614198912276234240)


@pytest.mark.release
@pytest.mark.devel
@pytest.mark.parametrize("position, pool", test_data)
def test_synth_math_amounts_from_price(position: LiquidityPosition, pool: PoolData):
    amount = get_amount0_from_price_range(
        p=test_position.current_price,
        pa=test_position.lower_price,
        pb=test_position.upper_price,
        amount1=test_position.amount1HR,
    )
    assert round(amount, 0) == test_position.amount0HR
    amount = get_amount1_from_price_range(
        p=test_position.current_price,
        pa=test_position.lower_price,
        pb=test_position.upper_price,
        amount0=test_position.amount0HR,
    )
    assert round(amount, 4) == round(test_position.amount1HR, 4)


@pytest.mark.release
@pytest.mark.devel
@pytest.mark.parametrize("position, pool", test_data)
def test_synth_math_amounts_from_tick(position: LiquidityPosition, pool: PoolData):
    amount = get_amount0_from_tick_range(
        p=position.current_price_x96,
        pa=get_sqrt_ratio_at_tick(position.lower_tick),
        pb=get_sqrt_ratio_at_tick(position.upper_tick),
        amount1=position.amount1,
    )
    assert round(amount / position.amount0, 18) == 1
    amount = get_amount1_from_tick_range(
        p=position.current_price_x96,
        pa=get_sqrt_ratio_at_tick(position.lower_tick),
        pb=get_sqrt_ratio_at_tick(position.upper_tick),
        amount0=position.amount0,
    )
    assert round(amount / position.amount1, 18) == 1


@pytest.mark.release
@pytest.mark.devel
@pytest.mark.parametrize("position, pool", test_data)
def test_synth__create_position_ticks(
    uni: UniswapV3, position: LiquidityPosition, pool: PoolData
):
    unchecked_pos_raw = uni.nft_position_manager._create_position(
        pool_data=pool,
        current_tick=position.current_tick,
        current_price_x96=position.current_price_x96,
        lower_tick=position.lower_tick,
        upper_tick=position.upper_tick,
        amount0=position.amount0,
    )
    assert round((unchecked_pos_raw.amount1 / position.amount1), 18) == 1
    unchecked_pos_raw = uni.nft_position_manager._create_position(
        pool_data=pool,
        current_tick=position.current_tick,
        current_price_x96=position.current_price_x96,
        lower_tick=position.lower_tick,
        upper_tick=position.upper_tick,
        amount1=position.amount1,
    )
    assert round((unchecked_pos_raw.amount0 / position.amount0), 18) == 1
    try:
        unchecked_pos_raw = uni.nft_position_manager._create_position(
            pool_data=pool,
            current_tick=position.current_tick,
            current_price_x96=position.current_price_x96,
            lower_tick=position.lower_tick,
            upper_tick=position.upper_tick,
        )
    except ValueError:
        pass
    except Exception:
        raise AssertionError


@pytest.mark.release
@pytest.mark.devel
@pytest.mark.parametrize("position, pool", test_data)
def test_synth_create_position(
    uni: UniswapV3, position: LiquidityPosition, pool: PoolData
):
    unchecked_pos = uni.nft_position_manager.create_position(
        pool_data=pool,
        current_price=position.current_price,
        lower_price=position.lower_price,
        upper_price=position.upper_price,
        amount0=position.amount0HR,
    )
    assert round(unchecked_pos.amount1HR / position.amount1HR, 2) == 1
    unchecked_pos = uni.nft_position_manager.create_position(
        pool_data=pool,
        current_price=position.current_price,
        lower_price=position.lower_price,
        upper_price=position.upper_price,
        amount1=position.amount1HR,
    )
    assert round(unchecked_pos.amount0HR / position.amount0HR, 2) == 1


@pytest.mark.release
@pytest.mark.devel
def test_mint_get_tx(uni: UniswapV3, pool_dai_weth: Pool):
    uc_position = uni.nft_position_manager.create_position(
        pool_data=pool_dai_weth.data,
        current_price=pool_dai_weth.data.token0Price,
        lower_price=pool_dai_weth.data.token0Price * 0.9,
        upper_price=pool_dai_weth.data.token0Price * 1.1,
        amount0=100,
    )

    tx_params = uni.nft_position_manager._get_mint_tx(
        token0=pool_dai_weth.data.token0.address,
        token1=pool_dai_weth.data.token1.address,
        fee=pool_dai_weth.data.immutables.fee,
        tick_lower=uc_position.raw.lower_tick,
        tick_upper=uc_position.raw.upper_tick,
        amount0=uc_position.adj_amount0,
        amount1=uc_position.adj_amount1,
        amount0_min=0,
        amount1_min=0,
    )
    assert tx_params.get("value") == 0
    assert tx_params.get("data", None) is not None
    decoded_params = uni.nft_position_manager.contract.decode_function_input(
        tx_params.get("data")
    )
    assert decoded_params[1]["params"]["tickLower"] == uc_position.raw.lower_tick
    assert decoded_params[1]["params"]["tickUpper"] == uc_position.raw.upper_tick


@pytest.mark.release
@pytest.mark.devel
def test_increase_liquidity_get_tx(uni: UniswapV3, pool_uni_weth: Pool):
    uc_position = uni.nft_position_manager.create_position(
        pool_data=pool_uni_weth.data,
        current_price=pool_uni_weth.data.token0Price,
        lower_price=pool_uni_weth.data.token0Price * 0.9,
        upper_price=pool_uni_weth.data.token0Price * 1.1,
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
    assert tx_params.get("data", None) is not None
    decoded_params = uni.nft_position_manager.contract.decode_function_input(
        tx_params.get("data")
    )
    assert decoded_params[1]["params"]["amount0Desired"] == uc_position.adj_amount0
    assert decoded_params[1]["params"]["amount1Desired"] == uc_position.adj_amount1


@pytest.mark.release
@pytest.mark.devel
def test_decrease_liquidity_get_tx(uni: UniswapV3):
    tx_params = uni.nft_position_manager._get_decrease_liquidity_tx(
        token_id=65590,
        liquidity=10,  # I took random number for testing purpose
        # better to fetch the liquidity with get_position and operate real number
        amount0_min=0,
        amount1_min=0,
    )
    assert tx_params.get("data", None) is not None
    decoded_params = uni.nft_position_manager.contract.decode_function_input(
        tx_params.get("data")
    )
    assert decoded_params[1]["params"]["liquidity"] == 10


@pytest.mark.release
@pytest.mark.devel
def test_collect_get_tx(uni: UniswapV3):
    tx_params = uni.nft_position_manager._get_collect_tx(
        token_id=65590,
    )
    assert tx_params.get("data", None) is not None
    decoded_params = uni.nft_position_manager.contract.decode_function_input(
        tx_params.get("data")
    )
    assert decoded_params[1]["params"]["tokenId"] == 65590


@pytest.mark.release
@pytest.mark.devel
def test_decrease_collect_get_tx(uni: UniswapV3):
    tx_params = uni.nft_position_manager._get_decrease_collect_tx(
        token_id=65590, liquidity=1, amount0_min=0, amount1_min=0
    )
    assert tx_params.get("data", None) is not None
    decoded_params = uni.nft_position_manager.decode_multicall(tx_params.get("data"))
    assert len(decoded_params) == 2
    assert decoded_params[0][0].fn_name == "decreaseLiquidity"
    assert decoded_params[1][0].fn_name == "collect"


@pytest.mark.release
def test_mint(uni: UniswapV3, pool_uni_weth: Pool):
    """
    Run real transaction with liquidity minting, but with
    a dummy data from the `pool_data`
    """
    uc_position = uni.nft_position_manager.create_position(
        pool_data=pool_uni_weth.data,
        current_price=pool_uni_weth.data.token0Price,
        lower_price=pool_uni_weth.data.token0Price * 0.9,
        upper_price=pool_uni_weth.data.token0Price * 1.1,
        amount0=0.01,
    )

    tx_receipt = uni.nft_position_manager.mint(
        unchecked_nft_position=uc_position, wait=True
    )
    print(tx_receipt)


@pytest.mark.release
def test_increase_liquidity(uni: UniswapV3, pool_uni_weth: Pool):
    """
    Run a real transaction with liquidity increase by 5 DAI,
    with a real data from Uniswap. It is unreal to increase liqudity
    with synthetic data as the pool change price in time.
    """
    # TODO: need to force update pool, if previously new position was minted
    # self._state = self._get_state()

    unchecked_pos = uni.nft_position_manager.create_position(
        pool_data=pool_uni_weth.data,
        current_price=pool_uni_weth.data.token0Price,
        lower_price=pool_uni_weth.data.token0Price * 0.9,
        upper_price=pool_uni_weth.data.token0Price * 1.1,
        amount0=0.01,
    )
    tx_receipt = uni.nft_position_manager.increase_liquidity(
        token_id=65590, unchecked_nft_position=unchecked_pos, wait=True
    )
    print(tx_receipt)


@pytest.mark.release
def test_decrease_liquidity(uni: UniswapV3, pool_uni_weth: Pool):
    pool = pool_uni_weth
    token_id = 65590
    tx_receipt = uni.nft_position_manager.decrease_liquidity(
        token_id=token_id, pool=pool, percent=0.3
    )
    print(tx_receipt)


@pytest.mark.release
def test_collect(uni: UniswapV3):
    token_id = 62537
    tx_receipt = uni.nft_position_manager.collect(token_id=token_id, wait=True)
    print(tx_receipt)


@pytest.mark.release
def test_decrease_collect(uni: UniswapV3, pool_uni_weth: Pool):
    pool = pool_uni_weth
    token_id = 62537
    tx_receipt = uni.nft_position_manager.decrease_collect(
        token_id=token_id, pool=pool, percent=0.2
    )
    print(tx_receipt)

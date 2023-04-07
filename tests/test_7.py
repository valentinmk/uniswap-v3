import pytest
from pprint import pp

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


def test_draft(uni):
    pass


def test_print_mint_sc_call(uni: UniswapV3):
    hex_data = "0x8831645600000000000000000000000011fe4b6ae13d2a6055c8d9cf65c55bac32b5d844000000000000000000000000b4fbf271143f4fbf7b91a5ded31805e42b2208d600000000000000000000000000000000000000000000000000000000000001f4fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe9350fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe93a00000000000000000000000000000000000000000000000008ac7230489e7fc250000000000000000000000000000000000000000000000000002834e49228be700000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000997d4c6a7ca5d524babdf1b205351f6fb623b5e700000000000000000000000000000000000000000000000000000000642a8f9c"  # noqa
    # call_data = uni.nft_position_manager.decode_multicall(hex_data)
    call_data = uni.nft_position_manager.contract.decode_function_input(hex_data)
    pp(call_data)


@pytest.mark.skip
def test_get_positions(uni: UniswapV3, weth: Token, dai: Token):
    pool_weth_dai = uni.get_pool(weth.address, dai.address, fee=500)
    pp(pool_weth_dai.data)


# tokens with same decimals
# Test with predefined data
# Example pool state
current_price_x96 = 745530830026153871741189246
current_tick = -93325
# Example position input params
current_price = 0.0000885466
# lower_price = 0.00009958175662218681  # 1 / 10042
# upper_price = 0.00009998000399920016  # 1 / 10002
lower_price = 0.000088233
upper_price = 0.000088941
lower_tick = -93360
upper_tick = -93280
amount0 = 9999999999999999013
amount1 = 707322211109863
amount0HR = 10
amount1HR = 0.000707322
# test pool data (it constantly changing in the testnet)
# for testing need we are fixed some state
pool_data = PoolData(
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


def test_synth_math_from_sqrtPriceX96():
    pp(from_sqrtPriceX96(current_price_x96))
    assert current_price == round(from_sqrtPriceX96(current_price_x96), 10)
    assert current_price != from_sqrtPriceX96(get_sqrt_ratio_at_tick(current_tick))
    assert current_price_x96 != get_sqrt_ratio_at_tick(current_tick)
    assert 5000 == from_sqrtPriceX96(5602277097478614198912276234240)


def test_synth_math_amounts_from_price():
    amount = get_amount0_from_price_range(
        p=current_price, pa=lower_price, pb=upper_price, amount1=amount1HR
    )
    assert round(amount, 0) == amount0HR
    amount = get_amount1_from_price_range(
        p=current_price, pa=lower_price, pb=upper_price, amount0=amount0HR
    )
    assert round(amount, 4) == round(amount1HR, 4)


def test_synth_math_amounts_from_tick():
    amount = get_amount0_from_tick_range(
        p=current_price_x96,
        pa=get_sqrt_ratio_at_tick(lower_tick),
        pb=get_sqrt_ratio_at_tick(upper_tick),
        amount1=amount1,
    )
    assert round(amount / amount0, 18) == 1
    amount = get_amount1_from_tick_range(
        p=current_price_x96,
        pa=get_sqrt_ratio_at_tick(lower_tick),
        pb=get_sqrt_ratio_at_tick(upper_tick),
        amount0=amount0,
    )
    assert round(amount / amount1, 18) == 1


def test_synth__create_position_ticks(uni: UniswapV3):
    unchecked_pos_raw = uni.nft_position_manager._create_position(
        pool_data=pool_data,
        current_tick=current_tick,
        current_price_x96=current_price_x96,
        lower_tick=lower_tick,
        upper_tick=upper_tick,
        amount0=amount0,
    )
    assert round((unchecked_pos_raw.amount1 / amount1), 18) == 1
    unchecked_pos_raw = uni.nft_position_manager._create_position(
        pool_data=pool_data,
        current_tick=current_tick,
        current_price_x96=current_price_x96,
        lower_tick=lower_tick,
        upper_tick=upper_tick,
        amount1=amount1,
    )
    assert round((unchecked_pos_raw.amount0 / amount0), 18) == 1
    try:
        unchecked_pos_raw = uni.nft_position_manager._create_position(
            pool_data=pool_data,
            current_tick=current_tick,
            current_price_x96=current_price_x96,
            lower_tick=lower_tick,
            upper_tick=upper_tick,
        )
    except ValueError:
        pass
    except Exception:
        raise AssertionError


def test_synth_create_position(uni: UniswapV3):
    unchecked_pos = uni.nft_position_manager.create_position(
        pool_data=pool_data,
        current_price=current_price,
        lower_price=lower_price,
        upper_price=upper_price,
        amount0=amount0HR,
    )
    assert round(unchecked_pos.amount1HR / amount1HR, 2) == 1
    pp(unchecked_pos)
    unchecked_pos = uni.nft_position_manager.create_position(
        pool_data=pool_data,
        current_price=current_price,
        lower_price=lower_price,
        upper_price=upper_price,
        amount1=amount1HR,
    )
    assert round(unchecked_pos.amount0HR / amount0HR, 2) == 1


@pytest.mark.skip
def test_synth_mint(uni: UniswapV3):
    """
    Run real transaction with liquidityy minting, but with
    a dummy data from the `pool_data`
    """
    unchecked_pos = uni.nft_position_manager.create_position(
        pool_data=pool_data,
        current_price=current_price,
        lower_price=lower_price,
        upper_price=upper_price,
        amount0=amount0HR,
    )
    transaction = uni.nft_position_manager.mint(unchecked_nft_position=unchecked_pos)
    pp(transaction)


@pytest.mark.skip
def test_real_mint(uni: UniswapV3, pool_dai_weth: Pool):
    """
    Run real transaction with liquidityy minting, but with
    a real data from Uniswap.
    """
    pool = pool_dai_weth
    unchecked_pos = uni.nft_position_manager.create_position(
        pool_data=pool.data,
        current_price=pool.data.token0Price,
        lower_price=pool.data.token0Price * 0.99,
        upper_price=pool.data.token0Price * 1.01,
        amount0=10,  # 10 DAI
    )
    transaction = uni.nft_position_manager.mint(unchecked_nft_position=unchecked_pos)
    pp(transaction)


@pytest.mark.skip
def test_real_increase_liquidity(uni: UniswapV3, pool_dai_weth: Pool):
    """
    Run a real transaction with liquidity increase by 5 DAI,
    with a real data from Uniswap. It is unreal to increase liqudity
    with synthetic data as the pool change price in time.
    """
    # TODO: need to force update pool, if previously new position was minted
    # self._state = self._get_state()
    pool = pool_dai_weth
    pool._state = pool._get_state()
    n_positions = uni.nft_position_manager._fetch_balance_of()
    last_position_id = uni.nft_position_manager._fetch_token_owner_by_index(
        n_positions - 1
    )
    last_position_raw = uni.nft_position_manager._fetch_position_info(last_position_id)
    last_position = uni.nft_position_manager._get_position(
        token_id=last_position_id, position_raw=last_position_raw, pool=pool
    )
    pp(last_position)
    unchecked_pos = uni.nft_position_manager.create_position(
        pool_data=last_position.pool,  # TODO: pool or PoolData ???
        current_price=last_position.pool.token0Price,
        lower_price=last_position.lower_price,
        upper_price=last_position.upper_price,
        amount0=5,  # add 5 DAI liquidity
        # amount1=0.000598268,
    )
    transaction = uni.nft_position_manager.increase_liquidity(
        token_id=last_position.token_id, unchecked_nft_position=unchecked_pos
    )
    pp(transaction)


@pytest.mark.skip
def test_real_decrease_liquidity(uni: UniswapV3, pool_dai_weth: Pool):
    pool = pool_dai_weth
    token_id = 62532
    transaction = uni.nft_position_manager.decrease_liquidity(
        token_id=token_id, pool=pool, percent=0.3
    )
    pp(transaction)


@pytest.mark.skip
def test_real_collect(uni: UniswapV3):
    token_id = 62537
    transaction = uni.nft_position_manager.collect(token_id=token_id)
    pp(transaction)


@pytest.mark.skip
def test_real_decrease_collect(uni: UniswapV3, pool_dai_weth: Pool):
    pool = pool_dai_weth
    token_id = 62537
    transaction = uni.nft_position_manager.decrease_collect(
        token_id=token_id, pool=pool, percent=0.2
    )
    pp(transaction)

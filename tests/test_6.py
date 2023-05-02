import pytest

from .helpers.models import LiquidityPosition

from uniswap.v3.main import UniswapV3
from uniswap.v3.models import Token, PoolData, PoolImmutablesRaw, PoolStateRaw
from uniswap.v3.math import (
    from_sqrtPriceX96,
    get_amount0,
    get_amount1,
    get_amount0_from_tick_range,
    get_amount1_from_tick_range,
    get_amount0_from_price_range,
    get_amount1_from_price_range,
    get_sqrt_ratio_at_tick,
    get_liquidity,
    get_tick_from_price,
    to_sqrtPriceX96,
    MAX_TICK,
    MIN_TICK,
)


test_cases_math = [
    LiquidityPosition(
        current_price_x96=67832069427941323875712969912,
        current_tick=-3107,
        current_price=0.7330118001653848,
        lower_price=0.50009,
        upper_price=1,
        lower_tick=-6930,
        upper_tick=0,
        amount0=112762257871693385,
        amount1=100000000000000000,
        liquidity=671185927217804975,
        amount0HR=0.112762,
        amount1HR=0.1,
    ),
    LiquidityPosition(
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
        liquidity=42361707494914999232,
        amount0HR=10,
        amount1HR=0.000707322,
    ),
]


@pytest.mark.release
@pytest.mark.devel
@pytest.mark.parametrize("test_case", test_cases_math)
def test_from_sqrtPriceX96(test_case: LiquidityPosition):
    assert round(test_case.current_price, 8) == round(
        from_sqrtPriceX96(test_case.current_price_x96), 8
    )
    # XXX
    # need to fix it
    assert (
        from_sqrtPriceX96(get_sqrt_ratio_at_tick(test_case.current_tick))
        / test_case.current_price
        > 0.9999
    )
    assert (
        round(to_sqrtPriceX96(test_case.current_price) / test_case.current_price_x96, 6)
        == 1
    )
    # https://uniswapv3book.com/docs/milestone_1/calculating-liquidity/"
    assert from_sqrtPriceX96(5602277097478614198912276234240) == 5000
    # XXX
    # Fuck it/me -  Current tick != current_price_x96 in common case !!!!
    # https://github.com/Uniswap/v3-core/blob/main/contracts/interfaces/pool/IUniswapV3PoolState.sol#L10  # noqa
    # /// @return sqrtPriceX96 The current price of the pool as a sqrt(token1/token0) Q64.96 value  # noqa
    # /// tick The current tick of the pool, i.e. according to the last tick transition that was run.  # noqa
    # /// This value may not always be equal to SqrtTickMath.getTickAtSqrtRatio(sqrtPriceX96) if the price is on a tick  # noqa
    # /// boundary.


@pytest.mark.release
@pytest.mark.devel
@pytest.mark.parametrize("test_case", test_cases_math)
def test_get_amount_from_price_range(test_case: LiquidityPosition):
    # TODO
    # XXX
    # Need to check here around min amount0HR and amount0HR_1
    amount0HR = get_amount0_from_price_range(
        p=test_case.current_price,
        pa=test_case.lower_price,
        pb=test_case.upper_price,
        amount1=test_case.amount1HR,
    ) / 10 ** (18 - 18)

    amount1HR = get_amount1_from_price_range(
        p=test_case.current_price,
        pa=test_case.lower_price,
        pb=test_case.upper_price,
        amount0=test_case.amount0HR,
    ) / 10 ** (18 - 18)

    amount0HR_1 = get_amount0_from_price_range(
        p=test_case.current_price,
        pa=test_case.lower_price,
        pb=test_case.upper_price,
        amount1=amount1HR,
    ) / 10 ** (18 - 18)
    assert round(test_case.amount0HR, 6) == round(min((amount0HR, amount0HR_1)), 6)
    assert round(test_case.amount1HR, 6) == round(amount1HR, 6)


@pytest.mark.release
@pytest.mark.devel
@pytest.mark.parametrize("test_case", test_cases_math)
def test_get_amount_from_tick_range(test_case: LiquidityPosition):
    amount0 = get_amount0_from_tick_range(
        p=test_case.current_price_x96,
        pa=get_sqrt_ratio_at_tick(test_case.lower_tick),
        pb=get_sqrt_ratio_at_tick(test_case.upper_tick),
        amount1=test_case.amount1,
    )

    amount1 = get_amount1_from_tick_range(
        p=test_case.current_price_x96,
        pa=get_sqrt_ratio_at_tick(test_case.lower_tick),
        pb=get_sqrt_ratio_at_tick(test_case.upper_tick),
        amount0=test_case.amount0,
    )
    assert abs(test_case.amount0 - amount0) in [0, 1]
    assert abs(test_case.amount1 - amount1) in [0, 1]


@pytest.mark.release
@pytest.mark.devel
@pytest.mark.parametrize("test_case", test_cases_math)
def test_get_liquidity(test_case: LiquidityPosition):
    liq = get_liquidity(
        sqrt_price_x_96=test_case.current_price_x96,
        sqrt_price_x_96_tick_lower=get_sqrt_ratio_at_tick(test_case.lower_tick),
        sqrt_price_x_96_tick_upper=get_sqrt_ratio_at_tick(test_case.upper_tick),
        amount0=test_case.amount0,
        amount1=test_case.amount1,
    )
    assert liq == test_case.liquidity
    # print(f"get_liquidity:{liq}")


test_cases_pos = [
    (
        LiquidityPosition(
            current_price_x96=867129379462269551444953425,
            current_tick=-90303,
            current_price=0.000119787,
            lower_price=0.00011958,
            upper_price=0.00012006,
            lower_tick=-90320,
            upper_tick=-90280,
            amount0=99999899999999995637,
            amount1=9324508230930832,
            liquidity=1,
            amount0HR=99.9999,
            amount1HR=0.0093245,
        ),
        PoolData(
            immutables=PoolImmutablesRaw(
                factory="0x1F98431c8aD98523631AE4a59f267346ea31F984",
                token0="0x11fE4B6AE13d2a6055C8D9cF65c55bac32B5d844",
                token1="0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6",
                fee=500,
                tickSpacing=10,
                maxLiquidityPerTick=1917569901783203986719870431555990,
            ),
            state=PoolStateRaw(
                liquidity=813812387392949047851,
                sqrtPriceX96=867129379462269551444953425,
                tick=-90303,
                observationIndex=394,
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
            token0Price=0.0001197867092845997,
            token1Price=8348.171562373525,
        ),
    ),
    (
        LiquidityPosition(
            current_price_x96=7377628838539388810461255126,
            current_tick=-47500,
            current_price=0.0086711,
            lower_price=0.0086538,
            upper_price=0.0086884,
            lower_tick=-47500,
            upper_tick=-47460,
            amount0=499998999999999940,
            amount1=4350967460805428,
            liquidity=1,
            amount0HR=0.499999,
            amount1HR=0.00435096,
        ),
        PoolData(
            immutables=PoolImmutablesRaw(
                factory="0x1F98431c8aD98523631AE4a59f267346ea31F984",
                token0="0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
                token1="0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6",
                fee=500,
                tickSpacing=10,
                maxLiquidityPerTick=1917569901783203986719870431555990,
            ),
            state=PoolStateRaw(
                liquidity=830998603102457143416,
                sqrtPriceX96=7377628838539388810461255126,
                tick=-47480,
                observationIndex=472,
                observationCardinality=500,
                observationCardinalityNext=500,
                feeProtocol=0,
                unlocked=True,
            ),
            token0=Token(
                chainId=5,
                decimals=18,
                symbol="UNI",
                name="Uniswap",
                isNative=False,
                isToken=True,
                address="0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
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
            address="0x07A4f63f643fE39261140DF5E613b9469eccEC86",
            token0Price=0.008671104846430388,
            token1Price=115.32555743593245,
        ),
    ),
    (
        LiquidityPosition(
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
        ),
        # test pool data (it constantly changing in the testnet)
        # for testing need we are fixed some state
        PoolData(
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
        ),
    ),
]


@pytest.mark.release
@pytest.mark.devel
def test_create_test_data(uni: UniswapV3, weth: Token, uni_token: Token, dai: Token):
    # weth_uni_pool = uni.get_pool(uni_token.address, weth.address, 500)
    # print(weth_uni_pool.data)
    # print(
    #     uni.nft_position_manager.contract.decode_function_input(
    #         "0x883164560000000000000000000000001f9840a85d5af5bf1d1762f925bdaddc4201f984000000000000000000000000b4fbf271143f4fbf7b91a5ded31805e42b2208d600000000000000000000000000000000000000000000000000000000000001f4ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff4674ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff469c00000000000000000000000000000000000000000000000006f05a70ff0cefc4000000000000000000000000000000000000000000000000000f752e8dee3b3400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000997d4c6a7ca5d524babdf1b205351f6fb623b5e700000000000000000000000000000000000000000000000000000000644fdfb4"  # noqa
    #     )
    # )
    # dai_weth_pool = uni.get_pool(dai.address, weth.address, 500)
    # print(dai_weth_pool.data)
    # print(
    #     uni.nft_position_manager.contract.decode_function_input(
    #         "0x8831645600000000000000000000000011fe4b6ae13d2a6055c8d9cf65c55bac32b5d844000000000000000000000000b4fbf271143f4fbf7b91a5ded31805e42b2208d600000000000000000000000000000000000000000000000000000000000001f4fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe9f30fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe9f580000000000000000000000000000000000000000000000056bc7033a5295aef50000000000000000000000000000000000000000000000000021209740cf519000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000997d4c6a7ca5d524babdf1b205351f6fb623b5e700000000000000000000000000000000000000000000000000000000644fe0ec"  # noqa
    #     )
    # )
    return


@pytest.mark.release
@pytest.mark.devel
@pytest.mark.parametrize("position, pool", test_cases_pos)
def test_create_position(uni: UniswapV3, position: LiquidityPosition, pool: PoolData):
    # print(position)
    # print(pool)

    unchecked_pos = uni.nft_position_manager.create_position(
        pool_data=pool,
        current_price=position.current_price,
        lower_price=position.lower_price,
        upper_price=position.upper_price,
        amount0=position.amount0HR,
    )
    # due to lower and upper price
    # provided with rounding
    # will result in bigger amounts
    assert 1.00001 > unchecked_pos.adj_amount0HR / position.amount0HR > 0.99999
    assert 1.00001 > unchecked_pos.adj_amount1HR / position.amount1HR > 0.99999


@pytest.mark.release
@pytest.mark.devel
@pytest.mark.parametrize("position, pool", test_cases_pos)
def test__create_position(uni: UniswapV3, position: LiquidityPosition, pool: PoolData):
    unchecked_pos_raw = uni.nft_position_manager._create_position(
        pool_data=pool,
        current_tick=position.current_tick,
        current_price_x96=position.current_price_x96,
        lower_tick=position.lower_tick,
        upper_tick=position.upper_tick,
        amount1=position.amount1,
    )
    assert abs(position.amount1 - unchecked_pos_raw.amount1) in [0, 1]
    unchecked_pos_raw = uni.nft_position_manager._create_position(
        pool_data=pool,
        current_tick=position.current_tick,
        current_price_x96=position.current_price_x96,
        lower_tick=position.lower_tick,
        upper_tick=position.upper_tick,
        amount0=position.amount0,
    )
    assert abs(position.amount1 - unchecked_pos_raw.amount1) in [0, 1]
    # print(unchecked_pos_raw)
    # due to lower and upper price
    # provided with rounding
    # will result in bigger amounts
    # assert unchecked_pos.adj_amount0HR >= position.amount0HR
    # assert unchecked_pos.adj_amount1HR >= position.amount1HR


@pytest.mark.release
@pytest.mark.devel
@pytest.mark.parametrize("position, pool", test_cases_pos)
def test_get_amount1(position: LiquidityPosition, pool: PoolData):
    # this way is not works well if you don't know both amount0 and amount1
    # in the same time
    # and it gives -1 difference as well
    liq = get_liquidity(
        sqrt_price_x_96=position.current_price_x96,
        sqrt_price_x_96_tick_lower=get_sqrt_ratio_at_tick(position.lower_tick),
        sqrt_price_x_96_tick_upper=get_sqrt_ratio_at_tick(position.upper_tick),
        amount0=position.amount0,
        amount1=position.amount1,
    )
    amount1_orig = get_amount1(
        position.current_tick,
        position.current_price_x96,
        position.lower_tick,
        position.upper_tick,
        liq,
    )
    amount0_orig = get_amount0(
        position.current_tick,
        position.current_price_x96,
        position.lower_tick,
        position.upper_tick,
        liq,
    )
    assert position.amount0 - amount0_orig == 1
    assert position.amount1 - amount1_orig == 1


@pytest.mark.release
@pytest.mark.devel
def test_math_unit():
    with pytest.raises(Exception) as exc:
        get_sqrt_ratio_at_tick(MAX_TICK + 1)
    assert str(exc.value) == "Invariant TICK"
    with pytest.raises(Exception) as exc:
        get_sqrt_ratio_at_tick(MIN_TICK - 1)
    assert str(exc.value) == "Invariant TICK"
    assert get_tick_from_price(0.7330118001653848) == -3106

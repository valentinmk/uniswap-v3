import os

# import pprint
from web3 import Web3

from uniswap.EtherClient import web3_client

# from uniswap.utils.consts import ERC20_TOKENS
# from uniswap.utils.erc20token import EIP20Contract
from uniswap.utils.erc20token_consts import (
    GOERLI_UNI_TOKEN,
    GOERLI_WETH_TOKEN,
    GOERLI_DAI_TOKEN,
)
from uniswap.v3.main import UniswapV3
from uniswap.v3.math import (
    from_sqrtPriceX96,
    get_amount0_from_tick_range,
    get_amount1_from_tick_range,
    get_amount0_from_price_range,
    get_amount1_from_price_range,
    get_sqrt_ratio_at_tick,
    get_liquidity,
    get_tick_from_price,
)


def test_draft():
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
    uni = UniswapV3(eth_client)

    # unit = EIP20Contract(eth_client, eth_client.w3, ERC20_TOKENS[5]["UNI"])
    # weth = EIP20Contract(eth_client, eth_client.w3, ERC20_TOKENS[5]["WETH"])

    # _position_raw = uni.nft_position_manager._fetch_position_info(37319)
    # pool = uni.get_pool(_position_raw.token0, _position_raw.token1, _position_raw.fee)
    # position = uni.nft_position_manager._get_position(
    #     token_id=37319, position_raw=_position_raw, pool=pool
    # )
    # Get data for testing
    pool = uni.get_pool(GOERLI_WETH_TOKEN.address, GOERLI_UNI_TOKEN.address, 500)
    print(pool.data)
    pool = uni.get_pool(GOERLI_WETH_TOKEN.address, GOERLI_DAI_TOKEN.address, 10000)
    print(pool.data)
    hex_data = "0xac9650d800000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000001e00000000000000000000000000000000000000000000000000000000000000164883164560000000000000000000000001f9840a85d5af5bf1d1762f925bdaddc4201f984000000000000000000000000b4fbf271143f4fbf7b91a5ded31805e42b2208d600000000000000000000000000000000000000000000000000000000000001f4ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe4ee000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001909cad14836649000000000000000000000000000000000000000000000000016345785d8a00000000000000000000000000000000000000000000000000000189acd745a3ea9e000000000000000000000000000000000000000000000000015e293ecd735612000000000000000000000000997d4c6a7ca5d524babdf1b205351f6fb623b5e700000000000000000000000000000000000000000000000000000000639c79ec00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000412210e8a00000000000000000000000000000000000000000000000000000000"  # noqa
    call_data = uni.nft_position_manager.decode_multicall(hex_data)
    print(call_data)
    # Test example (data)
    current_price_x96 = 67832069427941323875712969912
    current_tick = -3107
    #
    current_price = 0.7330118001653848
    lower_price = 0.50009
    upper_price = 1
    lower_tick = -6930
    upper_tick = 0
    amount0 = 112762257871693385
    amount1 = 100000000000000000
    amount0HR = 0.112762
    amount1HR = 0.1

    print(
        "current_price vs. from_sqrtPriceX96(current_price_x96):                    ",
        current_price,
        from_sqrtPriceX96(current_price_x96) * 10 ** (18 - 18),
    )
    print(
        "current_price vs. from_sqrtPriceX96(get_sqrt_ratio_at_tick(current_tick)): ",
        current_price,
        from_sqrtPriceX96(get_sqrt_ratio_at_tick(current_tick)) * 10 ** (18 - 18),
    )
    print(
        "current_price_x96 vs. get_sqrt_ratio_at_tick(current_tick):                ",
        current_price_x96,
        get_sqrt_ratio_at_tick(current_tick),
    )

    print("https://uniswapv3book.com/docs/milestone_1/calculating-liquidity/")
    print(
        "From ex price_to_sqrtp(5000) = 5602277097478614198912276234240",
        " vs from_sqrtPriceX96:    ",
        5000,
        from_sqrtPriceX96(5602277097478614198912276234240),
    )
    # XXX
    # Fuck it/me -  Current tick != current_price_x96 in common case !!!!
    # https://github.com/Uniswap/v3-core/blob/main/contracts/interfaces/pool/IUniswapV3PoolState.sol#L10  # noqa
    # /// @return sqrtPriceX96 The current price of the pool as a sqrt(token1/token0) Q64.96 value  # noqa
    # /// tick The current tick of the pool, i.e. according to the last tick transition that was run.  # noqa
    # /// This value may not always be equal to SqrtTickMath.getTickAtSqrtRatio(sqrtPriceX96) if the price is on a tick  # noqa
    # /// boundary.

    # Test 0. Calculate amount0 based on ticks and amount1
    print("Test 0.")
    print(f"Price: {from_sqrtPriceX96(current_price_x96) * 10 ** (18 - 18)}")
    print(
        get_amount0_from_price_range(
            p=current_price,
            pa=lower_price,
            pb=upper_price,
            amount1=amount1HR,
            # p=current_price_x96,
            # pa=get_sqrt_ratio_at_tick(lower_tick),
            # pb=get_sqrt_ratio_at_tick(upper_tick),
            # amount1=amount1,
        )
        / 10 ** (18 - 18)
    )
    print(
        get_amount1_from_price_range(
            p=current_price,
            pa=lower_price,
            pb=upper_price,
            amount0=amount0HR,
            # p=current_price_x96,
            # pa=get_sqrt_ratio_at_tick(lower_tick),
            # pb=get_sqrt_ratio_at_tick(upper_tick),
            # amount0=amount0,
        )
        / 10 ** (18 - 18)
    )

    # XXX Test 1.
    print("Test 1.")
    print(f"amount0:                        {amount0}")
    print(f"amount1:                        {amount1}")
    print(f"current_price_x96:              {current_price_x96}")
    print(f"sqrt_ratio_AX96:                {get_sqrt_ratio_at_tick(lower_tick)}")
    print(f"sqrt_ratio_BX96:                {get_sqrt_ratio_at_tick(upper_tick)}")
    print(
        "get_amount0_from_range:        ",
        get_amount0_from_tick_range(
            p=current_price_x96,
            pa=get_sqrt_ratio_at_tick(lower_tick),
            pb=get_sqrt_ratio_at_tick(upper_tick),
            amount1=amount1,
        ),
    )

    print(
        "get_amount1_from_range:        ",
        get_amount1_from_tick_range(
            p=current_price_x96,
            pa=get_sqrt_ratio_at_tick(lower_tick),
            pb=get_sqrt_ratio_at_tick(upper_tick),
            amount0=amount0,
        ),
    )

    # Test case 2.
    print("Test 2.")

    liq = get_liquidity(
        sqrt_price_x_96=current_price_x96,
        sqrt_price_x_96_tick_lower=get_sqrt_ratio_at_tick(lower_tick),
        sqrt_price_x_96_tick_upper=get_sqrt_ratio_at_tick(upper_tick),
        amount0=amount0,
        amount1=amount1,
    )
    print("get_liquidity:                 ", liq)

    print(call_data)

    # Test 3. nft_position_manager create_position / create UncheckedPosition
    current_price = 0.7330118001653848
    lower_price = 0.50009
    upper_price = 1
    amount0HR = 0.112762
    amount1HR = 0.1
    current_price_x96 = 67832069427941323875712969912
    current_tick = -3107
    lower_tick = -6930
    upper_tick = 0
    amount0 = 112762257871693385
    amount1 = 100000000000000000
    unchecked_pos = uni.nft_position_manager.create_position(
        pool=pool.data,
        current_price=0.7330118001653848,
        lower_price=0.50009,
        upper_price=1,
        amount1=0.1,
    )
    assert round(unchecked_pos.amount0HR, 6) == amount0HR

    unchecked_pos = uni.nft_position_manager.create_position(
        pool=pool.data,
        current_price=0.7330118001653848,
        lower_price=0.50009,
        upper_price=1,
        amount0=0.112762,
    )
    assert round(unchecked_pos.amount1HR, 6) == amount1HR
    try:
        unchecked_pos = uni.nft_position_manager.create_position(
            pool=pool.data,
            current_price=0.7330118001653848,
            lower_price=0.50009,
            upper_price=1,
        )
    except ValueError:
        pass
    except Exception:
        raise AssertionError
    # Test 4. nft_position_manager create_position / create UncheckedPositionRaw
    unchecked_pos_raw = uni.nft_position_manager._create_position(
        pool=pool.data,
        current_tick=current_tick,
        current_price_x96=current_price_x96,
        lower_tick=lower_tick,
        upper_tick=upper_tick,
        amount0=amount0,
    )
    assert unchecked_pos_raw.amount1 == amount1
    unchecked_pos_raw = uni.nft_position_manager._create_position(
        pool=pool.data,
        current_tick=current_tick,
        current_price_x96=current_price_x96,
        lower_tick=lower_tick,
        upper_tick=upper_tick,
        amount1=amount1,
    )
    assert unchecked_pos_raw.amount0 == amount0
    try:
        unchecked_pos_raw = uni.nft_position_manager._create_position(
            pool=pool.data,
            current_tick=current_tick,
            current_price_x96=current_price_x96,
            lower_tick=lower_tick,
            upper_tick=upper_tick,
        )
    except ValueError:
        pass
    except Exception:
        raise AssertionError
    # TEST 5.
    get_tick_from_price(0.7330118001653848, 18, 18)
    pass

import os

# import pprint
from web3 import Web3

from uniswap.EtherClient import web3_client
from uniswap.utils.consts import ERC20_TOKENS
from uniswap.utils.erc20token import EIP20Contract
from uniswap.utils.erc20token_consts import GOERLI_UNI_TOKEN, GOERLI_WETH_TOKEN
from uniswap.v3.main import UniswapV3
from uniswap.v3.math import (
    from_sqrtPriceX96,
    get_amount0_from_range,
    get_amount0hr_from_range,
    get_amount1_from_range,
    get_amount1hr_from_range,
    get_sqrt_ratio_at_tick,
    get_sqrt_ratio_at_tick_alt,
    get_amount0,
    get_amount1,
    get_liquidity,
    get_liquidity0,
    get_liquidity1,
)


def test_draft():
    MY_ADDRESS = Web3.toChecksumAddress("0x997d4c6A7cA5d524babDf1b205351f6FB623b5E7")

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

    unit = EIP20Contract(eth_client, eth_client.w3, ERC20_TOKENS[5]["UNI"])
    weth = EIP20Contract(eth_client, eth_client.w3, ERC20_TOKENS[5]["WETH"])

    # _position_raw = uni.nft_position_manager._fetch_position_info(37319)
    # pool = uni.get_pool(_position_raw.token0, _position_raw.token1, _position_raw.fee)
    # position = uni.nft_position_manager._get_position(
    #     token_id=37319, position_raw=_position_raw, pool=pool
    # )
    # Get data for testing
    pool = uni.get_pool(GOERLI_WETH_TOKEN.address, GOERLI_UNI_TOKEN.address, 500)
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
    print(
        "current_price_x96 vs. get_sqrt_ratio_at_tick_alt(current_tick):            ",
        current_price_x96,
        get_sqrt_ratio_at_tick_alt(current_tick),
    )
    print("https://uniswapv3book.com/docs/milestone_1/calculating-liquidity/")
    print(
        "From ex price_to_sqrtp(5000) = 5602277097478614198912276234240",
        " vs from_sqrtPriceX96:    ",
        5000,
        from_sqrtPriceX96(5602277097478614198912276234240),
    )
    print(
        "From ex price_to_tick(5000) = 85176 vs "
        "from_sqrtPriceX96(get_sqrt_ratio_at_tick(85176))):    ",
        5000,
        from_sqrtPriceX96(get_sqrt_ratio_at_tick_alt(85176)),
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
        get_amount0hr_from_range(
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
        get_amount1hr_from_range(
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
        get_amount0_from_range(
            p=current_price_x96,
            pa=get_sqrt_ratio_at_tick(lower_tick),
            pb=get_sqrt_ratio_at_tick(upper_tick),
            amount1=amount1,
        ),
    )

    print(
        "get_amount1_from_range:        ",
        get_amount1_from_range(
            p=current_price_x96,
            pa=get_sqrt_ratio_at_tick(lower_tick),
            pb=get_sqrt_ratio_at_tick(upper_tick),
            amount0=amount0,
        ),
    )

    # Test case from PDF. Test 2.
    # amount0 = 2
    # amount1 = 4000
    # current_price = 2000
    # pa = 1500
    # pb = 2500
    print("Test 2.")

    liq = get_liquidity(
        tick_current=current_tick,
        sqrt_price_x_96=current_price_x96,
        tick_lower=lower_tick,
        tick_upper=upper_tick,
        amount0=amount0,
        amount1=amount1,
    )
    print(
        "get_liquidity:                 ",
        liq,
    )
    print(
        "get_amount0 from liquiduty:    ",
        get_amount0(
            tick_current=current_tick,
            sqrt_price_x_96=current_price_x96,
            tick_lower=lower_tick,
            tick_upper=upper_tick,
            liquidity=liq,
        ),
    )
    print(
        "get_amount1 from liquiduty:    ",
        get_amount1(
            tick_current=current_tick,
            sqrt_price_x_96=current_price_x96,
            tick_lower=lower_tick,
            tick_upper=upper_tick,
            liquidity=liq,
        ),
    )
    print(
        "get_amount0 from liquiduty1:   ",
        get_amount0(
            tick_current=current_tick,
            sqrt_price_x_96=current_price_x96,
            tick_lower=lower_tick,
            tick_upper=upper_tick,
            liquidity=get_liquidity1(
                amount=amount1,
                pa=current_price_x96,
                pb=get_sqrt_ratio_at_tick(lower_tick),
            ),
        ),
    )
    print(
        "get_amount1 from liquiduty0:   ",
        get_amount1(
            tick_current=current_tick,
            sqrt_price_x_96=current_price_x96,
            tick_lower=lower_tick,
            tick_upper=upper_tick,
            liquidity=get_liquidity0(
                amount=amount0,
                pa=current_price_x96,
                pb=get_sqrt_ratio_at_tick(upper_tick),
            ),
        ),
    )

    # hex = "0x5ae401dc00000000000000000000000000000000000000000000000000000000637213cc000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000016000000000000000000000000000000000000000000000000000000000000000e404e45aaf0000000000000000000000008d9eac6f25470effd68f0ad22993cb2813c0c9b9000000000000000000000000b4fbf271143f4fbf7b91a5ded31805e42b2208d600000000000000000000000000000000000000000000000000000000000027100000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000ed2b525841adfc0000000000000000000000000000000000000000000000000000001f887563d56edbf000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004449404b7c00000000000000000000000000000000000000000000000001f887563d56edbf0000000000000000000000007c7429fa0083ab49a18fda9c83f38a6b129470f200000000000000000000000000000000000000000000000000000000"  # noqa
    # [print(i) for i in uni.swap_router_02.decode_multicall(hex)]
    print(call_data)

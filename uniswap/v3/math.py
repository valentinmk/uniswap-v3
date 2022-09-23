Q32 = 2**32
Q96 = 2**96
Q128 = 2**128
MAX_UINT_128 = 2**128 - 1
MAX_UINT_256 = 2**256 - 1
# 115792089237316195423570985008687907853269984665640564039457584007913129639935
MIN_TICK = -887272
MAX_TICK = -MIN_TICK


def from_sqrtPriceX96(value: int) -> float:
    return (value**2) / (2**192)


def mul_shift(val, mul_by):
    return (val * mul_by) // Q128


def get_sqrt_ratio_at_tick(tick):
    """
    Original Sol code:
    https://github.com/Uniswap/v3-core/blob/main/contracts/libraries/TickMath.sol#L23
    """
    valid = tick >= MIN_TICK and tick <= MAX_TICK
    if not valid:
        raise Exception("Invariant TICK")

    abs_tick = abs(tick)
    ratio = (
        int(0xFFFCB933BD6FAD37AA2D162D1A594001)
        if (abs_tick & 0x1) != 0
        else int(0x100000000000000000000000000000000)
    )

    if (abs_tick & int(0x2)) != 0:
        ratio = mul_shift(ratio, int(0xFFF97272373D413259A46990580E213A))
    if (abs_tick & int(0x4)) != 0:
        ratio = mul_shift(ratio, int(0xFFF2E50F5F656932EF12357CF3C7FDCC))
    if (abs_tick & int(0x8)) != 0:
        ratio = mul_shift(ratio, int(0xFFE5CACA7E10E4E61C3624EAA0941CD0))
    if (abs_tick & int(0x10)) != 0:
        ratio = mul_shift(ratio, int(0xFFCB9843D60F6159C9DB58835C926644))
    if (abs_tick & int(0x20)) != 0:
        ratio = mul_shift(ratio, int(0xFF973B41FA98C081472E6896DFB254C0))
    if (abs_tick & int(0x40)) != 0:
        ratio = mul_shift(ratio, int(0xFF2EA16466C96A3843EC78B326B52861))
    if (abs_tick & int(0x80)) != 0:
        ratio = mul_shift(ratio, int(0xFE5DEE046A99A2A811C461F1969C3053))
    if (abs_tick & int(0x100)) != 0:
        ratio = mul_shift(ratio, int(0xFCBE86C7900A88AEDCFFC83B479AA3A4))
    if (abs_tick & int(0x200)) != 0:
        ratio = mul_shift(ratio, int(0xF987A7253AC413176F2B074CF7815E54))
    if (abs_tick & int(0x400)) != 0:
        ratio = mul_shift(ratio, int(0xF3392B0822B70005940C7A398E4B70F3))
    if (abs_tick & int(0x800)) != 0:
        ratio = mul_shift(ratio, int(0xE7159475A2C29B7443B29C7FA6E889D9))
    if (abs_tick & int(0x1000)) != 0:
        ratio = mul_shift(ratio, int(0xD097F3BDFD2022B8845AD8F792AA5825))
    if (abs_tick & int(0x2000)) != 0:
        ratio = mul_shift(ratio, int(0xA9F746462D870FDF8A65DC1F90E061E5))
    if (abs_tick & int(0x4000)) != 0:
        ratio = mul_shift(ratio, int(0x70D869A156D2A1B890BB3DF62BAF32F7))
    if (abs_tick & int(0x8000)) != 0:
        ratio = mul_shift(ratio, int(0x31BE135F97D08FD981231505542FCFA6))
    if (abs_tick & int(0x10000)) != 0:
        ratio = mul_shift(ratio, int(0x9AA508B5B7A84E1C677DE54F3E99BC9))
    if (abs_tick & int(0x20000)) != 0:
        ratio = mul_shift(ratio, int(0x5D6AF8DEDB81196699C329225EE604))
    if (abs_tick & int(0x40000)) != 0:
        ratio = mul_shift(ratio, int(0x2216E584F5FA1EA926041BEDFE98))
    if (abs_tick & int(0x80000)) != 0:
        ratio = mul_shift(ratio, int(0x48A170391F7DC42444E8FA2))

    if tick > 0:
        ratio = MAX_UINT_256 // ratio

    if ratio % Q32 > 0:
        return (ratio // Q32) + 1
    else:
        return ratio // Q32


def get_amount0_delta(sqrt_ratio_ax_96, sqrt_ratio_bx_96, liquidity):
    if sqrt_ratio_ax_96 > sqrt_ratio_bx_96:
        sqrt_ratio_ax_96, sqrt_ratio_bx_96 = sqrt_ratio_bx_96, sqrt_ratio_ax_96

    numerator1 = liquidity << 96
    numerator2 = sqrt_ratio_bx_96 - sqrt_ratio_ax_96

    return ((numerator1 * numerator2) // sqrt_ratio_bx_96) // sqrt_ratio_ax_96


def get_amount0(
    tick_current: int,
    sqrt_price_x_96: int,
    tick_lower: int,
    tick_upper: int,
    liquidity: int,
) -> int:
    if tick_current < tick_lower:
        tick0ratio = get_sqrt_ratio_at_tick(tick_lower)
        tick1ratio = get_sqrt_ratio_at_tick(tick_upper)
    elif tick_current < tick_upper:
        tick0ratio = sqrt_price_x_96
        tick1ratio = get_sqrt_ratio_at_tick(tick_upper)
    else:
        return 0
    return get_amount0_delta(tick0ratio, tick1ratio, liquidity)


def get_amount1_delta(sqrt_ratio_ax_96, sqrt_ratio_bx_96, liquidity):
    if sqrt_ratio_ax_96 > sqrt_ratio_bx_96:
        sqrt_ratio_ax_96, sqrt_ratio_bx_96 = sqrt_ratio_bx_96, sqrt_ratio_ax_96

    ratio_diff = sqrt_ratio_bx_96 - sqrt_ratio_ax_96

    return (liquidity * ratio_diff) // Q96


def get_amount1(tick_current, sqrt_price_x_96, tick_lower, tick_upper, liquidity):
    if tick_current < tick_lower:
        return 0
    elif tick_current < tick_upper:
        tick0ratio = get_sqrt_ratio_at_tick(tick_lower)
        tick1ratio = sqrt_price_x_96
    else:
        tick0ratio = get_sqrt_ratio_at_tick(tick_lower)
        tick1ratio = get_sqrt_ratio_at_tick(tick_upper)
    return get_amount1_delta(tick0ratio, tick1ratio, liquidity)

"""
Notes
-----
Below implementation based on the great article of Atis Elsts.

.. [1] Atis Elsts "LIQUIDITY MATH IN UNISWAP V3",
    https://atiselsts.github.io/pdfs/uniswap-v3-liquidity-math.pdf, 2022


Implementation utilize description of liquidity based on book of
Ivan Kuznetsov and all https://github.com/Jeiwan/uniswapv3-book contributors.

.. [2] Source: https://uniswapv3book.com/docs/milestone_1/calculating-liquidity/


"""
from math import sqrt, log

Q32 = 2**32
Q96 = 2**96
Q128 = 2**128
MAX_UINT_128 = 2**128 - 1
MAX_UINT_256 = 2**256 - 1
MIN_TICK = -887272
MAX_TICK = -MIN_TICK


def from_sqrtPriceX96(sqrtPriceX96: int) -> float:
    """Return price by sqrtPriceX96"""
    return (sqrtPriceX96**2) / (2**192)


def to_sqrtPriceX96(price: float) -> int:
    """Return sqrtPriceX96 by the price"""
    return int(price**0.5 * 2**96)


def mul_shift(val, mul_by):
    return (val * mul_by) // Q128


def get_sqrt_ratio_at_tick(tick: int) -> int:
    """
    Get sqrtRatioX96 from a tick.
    Original code:
    https://github.com/Uniswap/v3-core/blob/main/contracts/libraries/TickMath.sol#L23

    Parameters
    ----------
    tick : int
        Value of the Tick

    Returns
    -------
    int
        sqrtRatioX96 of a Price for a provided tick

    Notes
    -----
    A Python equivalent don't give the same precision of the result.
    Its Python equivalent is::

        def get_sqrt_ratio_at_tick(tick):
            return int(sqrt(1.0001**tick) * Q96)

    """
    # XXX
    # https://github.com/Uniswap/v3-core/blob/main/contracts/interfaces/pool/IUniswapV3PoolState.sol#L10 # noqa
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


# TODO
# replace with own functions
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


def get_amount1(
    tick_current: int,
    sqrt_price_x_96: int,
    tick_lower: int,
    tick_upper: int,
    liquidity: int,
) -> int:
    if tick_current < tick_lower:
        return 0
    elif tick_current < tick_upper:
        tick0ratio = get_sqrt_ratio_at_tick(tick_lower)
        tick1ratio = sqrt_price_x_96
    else:
        tick0ratio = get_sqrt_ratio_at_tick(tick_lower)
        tick1ratio = get_sqrt_ratio_at_tick(tick_upper)
    return get_amount1_delta(tick0ratio, tick1ratio, liquidity)


def get_liquidity0(amount: int, pa: int, pb: int) -> int:
    """
    Get a liquidity by sqrt price range and an amount of the first asset.
    Implementation based on the article [2]_

    Notes
    -----

    """
    if pa > pb:
        pa, pb = pb, pa
    return int((amount * (pa * pb) // Q96) // (pb - pa))


def get_liquidity1(amount: int, pa: int, pb: int) -> int:
    """
    Get a liquidity by a range of sqrt prices and an amount of the second asset.
    Implementation based on the article [2]_
    """
    if pa > pb:
        pa, pb = pb, pa
    return int(amount * Q96 // (pb - pa))


def get_liquidity(
    sqrt_price_x_96: int,
    sqrt_price_x_96_tick_lower: int,
    sqrt_price_x_96_tick_upper: int,
    amount0: int,
    amount1: int,
) -> int:
    """
    Get liquidity of the position by a sqrt of a current price, a lower and upper and
    amounts of assets.
    Implementation based on the article [2]_

    Parameters
    ----------
    sqrt_price_x_96 : int
        current sqrtPriceX96
    sqrt_price_x_96_tick_lower : int
        sqrtPriceX96 at tick_lower
    sqrt_price_x_96_tick_upper : int
        sqrtPriceX96 at tick_upper
    amount0: int
        Amount of the first asset
    amount1: int
        Amount of the second asset

    Returns
    -------
    float
        Liquidity
    """
    pa = sqrt_price_x_96_tick_lower  # get_sqrt_ratio_at_tick(tick_lower)
    pb = sqrt_price_x_96_tick_upper  # get_sqrt_ratio_at_tick(tick_upper)
    pc = sqrt_price_x_96

    liq0 = get_liquidity0(amount0, pc, pb)
    liq1 = get_liquidity1(amount1, pc, pa)
    return int(min(liq0, liq1))


def get_amount0_from_price_range(p: float, pa: float, pb: float, amount1):
    """
    Get amount1 from price range and amount0.

    Formula (1) [1]_

    Parameters
    ----------
    p : float
        current Price
    pa : float
        price of a lowerTick
        (i.e.: `from_sqrtPriceX96(get_sqrt_ratio_at_tick(lower_tick))`)
    pb : float
        price of a a upperTick
        (i.e.: `from_sqrtPriceX96(get_sqrt_ratio_at_tick(upper_tick))`)
    amount0: float
        Amount of the first asset (not in Wei)

    Returns
    -------
    float
        Amount of the first asset
    """
    p = max(min(p, pb), pa)
    liquidity = amount1 / ((sqrt(p) - sqrt(pa)))  # Ref. [1] (8)
    amount0 = liquidity * ((sqrt(pb) - sqrt(p)) / (sqrt(p) * sqrt(pb)))  # (11)

    return amount0


def get_amount1_from_price_range(p: float, pa: float, pb: float, amount0: float):
    """
    Get amount1 from price range and amount1.

    3.2.1 Example 1: Amount of assets from a range [1]_

    Parameters
    ----------
    p : float
        current Price
    pa : float
        price of a lowerTick
        (i.e.: `from_sqrtPriceX96(get_sqrt_ratio_at_tick(lower_tick))`)
    pb : float
        price of a a upperTick
        (i.e.: `from_sqrtPriceX96(get_sqrt_ratio_at_tick(upper_tick))`)
    amount0: float
        Amount of the first asset (not in Wei)

    Returns
    -------
    float
        Amount of the second asset
    """
    p = max(min(p, pb), pa)
    liquidity_amount0 = (  # Ref. [1] (5)
        amount0 * (sqrt(p) * sqrt(pb)) / (sqrt(pb) - sqrt(p))
    )
    amount1 = liquidity_amount0 * (sqrt(p) - sqrt(pa))
    return amount1


def get_amount0_from_tick_range(p: int, pa: int, pb: int, amount1: int) -> int:
    """
    Get amount1 from a tick range and amount0.

    Formula (1) [1]_

    Parameters
    ----------
    p : int
        sqrtRatioX96 of current Price
    pa : int
        sqrtRatioX96 from a lowerTick (sqrtRatioAX96)
    pb : int
        sqrtRatioX96 from a upperTick (sqrtRatioAX96)
    amount1: int
        Amount of the second asset in Wei

    Returns
    -------
    int
        Amount of the first asset in Wei
    """
    p = max(min(p, pb), pa)

    # liquidity_amount1 = (amount1 * Q96) // (p - pa)  # Ref. [1] (8)
    liquidity_amount1 = get_liquidity1(amount1, pa, p)
    amount0 = (liquidity_amount1 * Q96) * (pb - p) // (p * pb)  # (11)

    return amount0


def get_amount1_from_tick_range(p: int, pa: int, pb: int, amount0: int) -> int:
    """
    Get amount1 from tick range and amount1.

    3.2.1 Example 1: Amount of assets from a range [1]_

    Parameters
    ----------
    p : int
        sqrtRatioX96 of current Price
    pa : int
        sqrtRatioX96 from a lowerTick (sqrtRatioAX96)
    pb : int
        sqrtRatioX96 from a upperTick (sqrtRatioAX96)
    amount0: int
        Amount of the first asset in Wei

    Returns
    -------
    int
        Amount of the second asset in Wei
    """
    p = max(min(p, pb), pa)
    # liquidity_amount0 = (amount0 * (p * pb) / Q96) / (pb - p)  # Ref. [1] (5)
    liquidity_amount0 = get_liquidity0(amount0, p, pb)
    amount1 = liquidity_amount0 * (p - pa) / Q96
    return int(amount1)


def get_tick_from_price(price: float) -> int:
    """Return tick by provided price

    Parameters
    ----------
    price : float
        price

    Returns
    -------
    int
        Tick
    """
    tick = log(price, 1.0001)
    return int(round(tick, 0))

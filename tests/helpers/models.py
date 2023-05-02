from dataclasses import dataclass


@dataclass
class LiquidityPosition:
    # Test example (data)
    current_price_x96: int
    current_tick: int
    # HR
    current_price: float
    lower_price: float
    upper_price: float
    lower_tick: int
    upper_tick: int
    amount0: int
    amount1: int
    liquidity: int
    amount0HR: float
    amount1HR: float

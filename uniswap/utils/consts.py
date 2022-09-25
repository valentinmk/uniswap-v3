from web3 import Web3

MAINNET = 1
ROPSTEN = 3

EXACT_INPUT = 0
EXACT_OUTPUT = 1

ERC20_TOKENS = {
    MAINNET: {
        "USDC": Web3.toChecksumAddress("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"),
        "WETH": Web3.toChecksumAddress("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"),
    },
    ROPSTEN: {
        "USDC": Web3.toChecksumAddress("0x07865c6E87B9F70255377e024ace6630C1Eaa37F"),
        "WETH": Web3.toChecksumAddress("0xc778417E063141139Fce010982780140Aa0cD5Ab"),
        "UNI": Web3.toChecksumAddress("0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"),
        "AAVE": Web3.toChecksumAddress("0xa17669420eD99FAc51308567B08B7BaC86837BAf"),
        "COMP": Web3.toChecksumAddress("0xf76D4a441E4ba86A923ce32B89AFF89dBccAA075"),
    },
}


CONTRACT_ADDRESSES = {
    MAINNET: {
        "factory": Web3.toChecksumAddress("0x1F98431c8aD98523631AE4a59f267346ea31F984"),
        "nonfungible_position_manager": Web3.toChecksumAddress(
            "0xC36442b4a4522E871399CD717aBDD847Ab11FE88"
        ),
        "quoter": Web3.toChecksumAddress("0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6"),
        "swap_router": Web3.toChecksumAddress(
            "0xE592427A0AEce92De3Edee1F18E0157C05861564"
        ),
        # https://github.com/Uniswap/swap-router-contracts/blob/main/contracts/SwapRouter02.sol
        "swap_router_02": Web3.toChecksumAddress(
            "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45"
        ),
        "non_fungible_position_manager": Web3.toChecksumAddress(
            "0xC36442b4a4522E871399CD717aBDD847Ab11FE88"
        ),
    },
    ROPSTEN: {
        "factory": Web3.toChecksumAddress("0x1F98431c8aD98523631AE4a59f267346ea31F984"),
        "nonfungible_position_manager": Web3.toChecksumAddress(
            "0xC36442b4a4522E871399CD717aBDD847Ab11FE88"
        ),
        "quoter": Web3.toChecksumAddress("0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6"),
        "swap_router": Web3.toChecksumAddress(
            "0xE592427A0AEce92De3Edee1F18E0157C05861564"
        ),
        "swap_router_02": Web3.toChecksumAddress(
            "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45"
        ),
        "non_fungible_position_manager": Web3.toChecksumAddress(
            "0xC36442b4a4522E871399CD717aBDD847Ab11FE88"
        ),
    },
}

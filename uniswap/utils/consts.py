from web3 import Web3

MAINNET = 1
ROPSTEN = 3  # Discontinued 5th of October 2022
GOERLI = 5

EXACT_INPUT = 0
EXACT_OUTPUT = 1

ERC20_TOKENS = {
    MAINNET: {
        "USDC": Web3.to_checksum_address("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"),
        "WETH": Web3.to_checksum_address("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"),
    },
    GOERLI: {
        "USDC": Web3.to_checksum_address("0x07865c6E87B9F70255377e024ace6630C1Eaa37F"),
        "WETH": Web3.to_checksum_address("0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6"),
        "UNI": Web3.to_checksum_address("0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"),
        "AAVE": Web3.to_checksum_address("0x63242B9Bd3C22f18706d5c4E627B4735973f1f07"),
        "COMP": Web3.to_checksum_address("0x3587b2F7E0E2D6166d6C14230e7Fe160252B0ba4"),
        "DAI": Web3.to_checksum_address("0x11fE4B6AE13d2a6055C8D9cF65c55bac32B5d844"),
    },
}


CONTRACT_ADDRESSES = {
    MAINNET: {
        "factory": Web3.to_checksum_address(
            "0x1F98431c8aD98523631AE4a59f267346ea31F984"
        ),
        "nonfungible_position_manager": Web3.to_checksum_address(
            "0xC36442b4a4522E871399CD717aBDD847Ab11FE88"
        ),
        "quoter": Web3.to_checksum_address(
            "0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6"
        ),
        "swap_router": Web3.to_checksum_address(
            "0xE592427A0AEce92De3Edee1F18E0157C05861564"
        ),
        # https://github.com/Uniswap/swap-router-contracts/blob/main/contracts/SwapRouter02.sol
        "swap_router_02": Web3.to_checksum_address(
            "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45"
        ),
        "non_fungible_position_manager": Web3.to_checksum_address(
            "0xC36442b4a4522E871399CD717aBDD847Ab11FE88"
        ),
        "multicall2": Web3.to_checksum_address(
            "0x5BA1e12693Dc8F9c48aAD8770482f4739bEeD696"
        ),
    },
    GOERLI: {
        "factory": Web3.to_checksum_address(
            "0x1F98431c8aD98523631AE4a59f267346ea31F984"
        ),
        "nonfungible_position_manager": Web3.to_checksum_address(
            "0xC36442b4a4522E871399CD717aBDD847Ab11FE88"
        ),
        "quoter": Web3.to_checksum_address(
            "0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6"
        ),
        "swap_router": Web3.to_checksum_address(
            "0xE592427A0AEce92De3Edee1F18E0157C05861564"
        ),
        "swap_router_02": Web3.to_checksum_address(
            "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45"
        ),
        "non_fungible_position_manager": Web3.to_checksum_address(
            "0xC36442b4a4522E871399CD717aBDD847Ab11FE88"
        ),
        "multicall2": Web3.to_checksum_address(
            "0x5BA1e12693Dc8F9c48aAD8770482f4739bEeD696"
        ),
    },
}

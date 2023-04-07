# uniswap-v3

## WORK IN PROGRESS

An unofficial python client for Uniswap V3, built for human beings.

## TODO

1. version 0.0.1 - swaps

> You are here

- [x] Base classes
- [x] Original scenarios from an official documentations
  - [x] "Creating a Pool instance"
  - [x] "Fetching Spot Prices"
  - [x] "Creating a Trade"
  - [x] (Extra) Execute a Trade

1. version 0.0.2 - Position NFTs

- [x] Mint
- [x] Increase liquidity
- [x] Decrease liquidity
- [x] Collect
- [x] Position info
- [ ] "Swap and Add Liquidity Atomically" (?)

1. version 0.0.3 - multicall support

- [x] multicall interface

1. version 0.0.4 - Position NFT for humans

- [x] Mint
- [x] Increase liquidity
- [x] Decrease liquidity
- [x] Collect
- [x] Position info

1. version 0.0.5 - library design - client to BaseContract

- [ ] send_transaction to BaseContract
- [ ] multicall2 to lower RPS to provider
- [ ] multiple providers

1. version 0.0.6 - Position NFT for humans

- [ ] mint for Humans with the corner cases with ETH -> WETH
- [ ] test for the mint for Humans around pair with different decimals like ETH-USDT (18 vs 6?)
- [ ] increase liquidity with the corner cases with ETH -> WETH
- [ ] decrease liquidity with the corner cases with ETH -> WETH
- [ ] collect liquidity with the corner cases with ETH -> WETH

1. version 0.0.7 - PYPI publishing and docs

1. version 0.0.8 - finish with tests
1. version 0.0.9 - smart-routing / analog to AlphaRouter

- [ ] "Integrating the Auto Router"

## Hints

Use `export $(cat _.env | xargs)` to load yours `_.env` file in the terminal.
> END
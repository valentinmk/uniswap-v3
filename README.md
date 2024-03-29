# uniswap-v3

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg?logo=python)](https://www.python.org/downloads/release/python-310/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg?logo=python)](https://www.python.org/downloads/release/python-311/)

[![Pytest](https://github.com/valentinmk/uniswap-v3/actions/workflows/pytest.yaml/badge.svg)](https://github.com/valentinmk/uniswap-v3/actions)

[![Documentation Status](https://readthedocs.org/projects/uniswap-v3/badge/?version=latest)](https://uniswap-v3.readthedocs.io/en/latest/?badge=latest)

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
- [ ] multicall2 to decrease RPS of provider
- [ ] multiple providers

1. version 0.0.6 - Position NFT for humans

- [ ] mint for Humans with the corner cases with ETH -> WETH
- [ ] test for the mint for Humans around pair with different decimals like ETH-USDT (18 vs 6?)
- [ ] increase liquidity with the corner cases with ETH -> WETH
- [ ] decrease liquidity with the corner cases with ETH -> WETH
- [ ] collect liquidity with the corner cases with ETH -> WETH

1. version 0.0.7 - PYPI publishing and docs

1. version 0.0.8 - finish with tests
1. version 0.0.9 - smart-routing / similar to AlphaRouter

- [ ] "Integrating the Auto Router"

## Development Guide (sort of)

### Hints

Use `export $(cat _.env | xargs)` to load yours `_.env` file in the terminal.
> END

### Testing

Before testing run `pip install -r requirements_dev.txt`.
Runs with `pytest -vs tests/test_3.py -m devel --cov uniswap`.
For main branch releases will be executed via `pytest tests -m release --cov uniswap`.
Please check `tests/conftest.py` and `pytest.ini` for details.

### Docs

Notes:

- To collect docs from docstrings: `sphinx-apidoc -o source ../uniswap -M -f`
- To clean and build docs: `make clean && make html`

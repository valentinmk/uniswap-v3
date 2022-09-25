from eth_typing import ChecksumAddress
from uniswap.EtherClient.web3_client import EtherClient
from uniswap.utils.helpers import decode_nft_URI
from uniswap.v3.models import NftPosition, NftPositionRaw, NftPositionUriData
from uniswap.v3.math import get_amount0, get_amount1, MAX_UINT_128
from uniswap.v3.pool import Pool
from web3 import Web3

from .base import BaseContract


class NonfungiblePositionManager(BaseContract):
    """NonfungiblePositionManager.

    Deployment address: https://docs.uniswap.org/protocol/reference/deployments

    Original source code: https://github.com/Uniswap/v3-periphery/blob/v1.0.0/contracts/NonfungiblePositionManager.sol
    """  # noqa

    def __init__(
        self,
        client: EtherClient,
        w3: Web3,
        address: ChecksumAddress,
        abi_path: str = "../utils/abis/nft_position_manager.abi.json",
    ):
        super().__init__(w3, address, abi_path)
        self.client = client
        self._data = None

    def _get_data(self):
        raise NotImplementedError

    @property
    def data(self):
        """Get human readable information from pool"""
        if self._data is None:
            self._data = self._get_data()
        return self._data

    def decode_multicall(self, payload):
        function_name, data = self.contract.decode_function_input(payload)
        assert (
            function_name != "<Function multicall(bytes[])>"
        ), f"Not a multicall (function_name = {function_name})"
        data = data.get("data")
        return [self.contract.decode_function_input(i) for i in data]

    def _fetch_balance_of(self) -> int:
        return self.functions.balanceOf(self.client.address).call()

    def _fetch_token_owner_by_index(self, index: int):
        return self.functions.tokenOfOwnerByIndex(self.client.address, index).call()

    def _fetch_token_uri(self, token_id: int) -> NftPositionRaw:
        data = decode_nft_URI(self.functions.tokenURI(token_id).call())
        return NftPositionUriData(
            name=data.get("name"),
            description=data.get("description"),
            image=data.get("image"),
        )

    def _fetch_position_info(self, token_id: int) -> NftPositionRaw:
        (
            nonce,
            operator,
            token0,
            token1,
            fee,
            tickLower,
            tickUpper,
            liquidity,
            feeGrowthInside0LastX128,
            feeGrowthInside1LastX128,
            tokensOwed0,
            tokensOwed1,
        ) = self.functions.positions(token_id).call()
        return NftPositionRaw(
            token_id=token_id,
            nonce=nonce,
            operator=operator,
            token0=token0,
            token1=token1,
            fee=fee,
            tickLower=tickLower,
            tickUpper=tickUpper,
            liquidity=liquidity,
            feeGrowthInside0LastX128=feeGrowthInside0LastX128,
            feeGrowthInside1LastX128=feeGrowthInside1LastX128,
            tokensOwed0=tokensOwed0,
            tokensOwed1=tokensOwed1,
            token_URI_data=None,
        )

    def _get_position(
        self, token_id: int, position_raw: NftPositionRaw, pool: Pool
    ) -> NftPosition:
        amount0 = get_amount0(
            pool.data.state.tick,
            pool.data.state.sqrtPriceX96,
            position_raw.tickLower,
            position_raw.tickUpper,
            position_raw.liquidity,
        )
        amount0HR = amount0 / 10**pool.data.token0.decimals
        amount1 = get_amount1(
            pool.data.state.tick,
            pool.data.state.sqrtPriceX96,
            position_raw.tickLower,
            position_raw.tickUpper,
            position_raw.liquidity,
        )
        amount1HR = amount1 / 10**pool.data.token1.decimals
        unclaimedfeesamount0, unclaimedfeesamount1 = self.functions.collect(
            (
                token_id,
                self.client.address,
                MAX_UINT_128,
                MAX_UINT_128,
            )
        ).call()
        unclaimedfeesamount0HR = unclaimedfeesamount0 / 10**pool.data.token0.decimals
        unclaimedfeesamount1HR = unclaimedfeesamount1 / 10**pool.data.token1.decimals
        return NftPosition(
            token_id=token_id,
            raw=position_raw,
            pool=pool.data,
            amount0=amount0,
            amount1=amount1,
            amount0HR=amount0HR,
            amount1HR=amount1HR,
            unclaimedfeesamount0=unclaimedfeesamount0,
            unclaimedfeesamount1=unclaimedfeesamount1,
            unclaimedfeesamount0HR=unclaimedfeesamount0HR,
            unclaimedfeesamount1HR=unclaimedfeesamount1HR,
            token0=pool.data.token0,
            token1=pool.data.token1,
            fee=pool.data.immutables.fee / 10_000,
        )

    # def get_position(self, position_raw: NftPositionRaw) -> Position:

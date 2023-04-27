from eth_typing import ChecksumAddress
from uniswap.EtherClient.web3_client import EtherClient
from web3 import Web3

from ..utils.consts import CONTRACT_ADDRESSES
from .factory import Factory
from .pool import Pool
from .quoter import Quoter
from .swap_router import SwapRouter
from .swap_router_02 import SwapRouter02
from .nft_position_manager import NonfungiblePositionManager
from .multicall2 import Multicall2


class UniswapV3:
    """
    Module to interact with Uniswap v3 smart contracts.
    """

    def __init__(self, client: EtherClient) -> None:
        """
        Module to interact with Uniswap v3 smart contracts.

        Parameters
        ----------
        client : EtherClient
            EtherClient Client

        Returns
        -------
        UniswapV3
        """
        self.client: EtherClient = client
        self.w3: Web3 = client.w3
        self._factory: Factory = None
        self._quoter: Quoter = None
        self._swap_router: SwapRouter = None
        self._swap_router_02: SwapRouter02 = None
        self._nft_position_manager: NonfungiblePositionManager = None
        self._multicall2: Multicall2 = None

    @property
    def factory(self):
        if self._factory is None:
            self._factory = Factory(
                self.w3, CONTRACT_ADDRESSES[self.w3.eth.chain_id]["factory"]
            )
        return self._factory

    @property
    def quoter(self):
        if self._quoter is None:
            self._quoter = Quoter(
                self.w3, CONTRACT_ADDRESSES[self.w3.eth.chain_id]["quoter"]
            )
        return self._quoter

    @property
    def swap_router(self):
        if self._swap_router is None:
            self._swap_router = SwapRouter(
                self.w3, CONTRACT_ADDRESSES[self.w3.eth.chain_id]["swap_router"]
            )
        return self._swap_router

    @property
    def swap_router_02(self):
        if self._swap_router_02 is None:
            self._swap_router_02 = SwapRouter02(
                self.client,
                CONTRACT_ADDRESSES[self.w3.eth.chain_id]["swap_router_02"],
            )
        return self._swap_router_02

    @property
    def nft_position_manager(self):
        if self._nft_position_manager is None:
            self._nft_position_manager = NonfungiblePositionManager(
                self.client,
                self.w3,
                CONTRACT_ADDRESSES[self.w3.eth.chain_id][
                    "non_fungible_position_manager"
                ],
            )
        return self._nft_position_manager

    @property
    def multicall2(self):
        if self._multicall2 is None:
            self._multicall2 = Multicall2(
                self.client,
                self.w3,
                CONTRACT_ADDRESSES[self.w3.eth.chain_id]["multicall2"],
            )
        return self._multicall2

    @staticmethod
    def is_fee_valid(fee: int) -> bool:
        return fee in [100, 500, 3000, 10000]

    def get_pool(
        self, token0: ChecksumAddress, token1: ChecksumAddress, fee: int
    ) -> Pool:
        """
        Return the Pool contract wrapper.
        Please refer official documentation:
        https://docs.uniswap.org/contracts/v3/reference/core/UniswapV3Pool

        Parameters
        ----------
        token0 : ChecksumAddress
            Token0 contract address
        token1 : ChecksumAddress
            Token1 contract address
        fee: int
            Fee of the pool

        Returns
        -------
        `Pool`
        """
        if self.is_fee_valid(fee):
            pool_address = self.factory.functions.getPool(token0, token1, fee).call()
            return Pool(client=self.client, address=pool_address)
        else:
            raise BaseException("Invalid fee. Should be in [100, 500, 3000, 10000]")

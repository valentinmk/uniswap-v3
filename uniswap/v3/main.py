from web3 import Web3

from uniswap.EtherClient.web3_client import EtherClient


from ..utils.consts import CONTRACT_ADDRESSES
from .factory import Factory
from .pool import Pool
from .quoter import Quoter
from .swap_router import SwapRouter
from .swap_router_02 import SwapRouter02
from eth_typing import ChecksumAddress


class UniswapV3:
    def __init__(self, client: EtherClient) -> None:
        self.client: EtherClient = client
        self.w3: Web3 = client.w3
        self._factory: Factory = None
        self._quoter: Quoter = None
        self._swap_router: SwapRouter = None
        self._swap_router_02: SwapRouter02 = None

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
                self.w3,
                CONTRACT_ADDRESSES[self.w3.eth.chain_id]["swap_router_02"],
            )
        return self._swap_router_02

    @staticmethod
    def is_fee_valid(fee: int) -> bool:
        return fee in [100, 500, 3000, 10000]

    def get_pool(
        self, token0: ChecksumAddress, token1: ChecksumAddress, fee: int
    ) -> Pool:
        if self.is_fee_valid(fee):
            pool_address = self.factory.functions.getPool(token0, token1, fee).call()
            return Pool(client=self.client, w3=self.w3, address=pool_address)
        else:
            raise BaseException("Invalid fee. Should be in [500, 3000, 10000]")

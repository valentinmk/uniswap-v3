from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from web3 import Web3
from web3.types import TxReceipt, TxParams

from uniswap.EtherClient.web3_client import EtherClient
from uniswap.utils.helpers import decode_nft_URI, normalize_tick_by_spacing
from uniswap.v3.math import (
    MAX_UINT_128,
    get_sqrt_ratio_at_tick,
    get_amount0,
    get_amount0_from_price_range,
    get_amount0_from_tick_range,
    get_amount1,
    get_amount1_from_price_range,
    get_amount1_from_tick_range,
    get_tick_from_price,
)
from uniswap.v3.models import (
    NftPosition,
    NftPositionRaw,
    NftPositionUriData,
    PoolData,
    UncheckedNftPosition,
    UncheckedNftPositionRaw,
)
from uniswap.v3.pool import Pool

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

    def _fetch_token_owner_by_index(self, index: int, address=None):
        if not address:
            address = self.client.address
        return self.functions.tokenOfOwnerByIndex(address, index).call()

    def _fetch_token_uri(self, token_id: int) -> NftPositionUriData:
        """Run the tokenURI function.

        Parameters
        ----------
        token_id : int
            Id of the nft position.

        Returns
        -------
        NftPositionUriData
        """
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
        """Run the positions function.

        Parameters
        ----------
        token_id : int
            Id of the nft position.

        Returns
        -------
        NftPositionRaw - token information with raw data from protocol
        """
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
            token_URI_data=self._fetch_token_uri(token_id=token_id),
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
            lower_price=1.0001**position_raw.tickLower,
            upper_price=1.0001**position_raw.tickUpper,
            lower_price_inverse=1 / 1.0001**position_raw.tickLower,
            upper_price_inverse=1 / 1.0001**position_raw.tickUpper,
            unclaimedfeesamount0=unclaimedfeesamount0,
            unclaimedfeesamount1=unclaimedfeesamount1,
            unclaimedfeesamount0HR=unclaimedfeesamount0HR,
            unclaimedfeesamount1HR=unclaimedfeesamount1HR,
            token0=pool.data.token0,
            token1=pool.data.token1,
            fee=pool.data.immutables.fee / 10_000,
        )

    def sign_tx(self, transaction):
        private_key = self.w3.eth.account.decrypt(
            self.client._keyfile_json, self.client._wallet_pass
        )
        signed_tx = self.client.w3.eth.account.sign_transaction(
            transaction, private_key
        )
        return signed_tx

    def send_tx(self, signed_transaction, wait: bool = False) -> HexBytes | TxReceipt:
        tx_hash = self.w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
        if wait:
            return self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_hash

    def _get_mint_tx(
        self,
        token0: ChecksumAddress,
        token1: ChecksumAddress,
        fee: int,
        tick_lower: int,
        tick_upper: int,
        amount0: int,
        amount1: int,
        amount0_min: int,
        amount1_min: int,
        recipient: ChecksumAddress = None,
        deadline: int = 2**64,
    ) -> TxParams:
        """Create Mint transaction

        For mint params refer: https://github.com/Uniswap/v3-periphery/blob/main/contracts/interfaces/INonfungiblePositionManager.sol#L79
        """  # noqa
        function_call = self.functions.mint(
            (
                token0,
                token1,
                fee,
                tick_lower,
                tick_upper,
                amount0,
                amount1,
                amount0_min,
                amount1_min,
                recipient if recipient else self.client.address,
                deadline,
            )
        )
        transaction = function_call.build_transaction(
            {
                "chainId": self.w3.eth.chain_id,
                "from": self.client.address,
                "nonce": self.w3.eth.get_transaction_count(self.client.address),
            }
        )
        return transaction

    def _get_increase_liquidity_tx(
        self,
        token_id: int,
        amount0: int,
        amount1: int,
        amount0_min: int,
        amount1_min: int,
        deadline: int = 2**64,
        wait=False,
    ) -> TxParams:
        """Increase liquidity

        For Increase liquidity params refer: https://github.com/Uniswap/v3-periphery/blob/main/contracts/interfaces/INonfungiblePositionManager.sol#L111
        """  # noqa
        function_call = self.functions.increaseLiquidity(
            (
                token_id,
                amount0,
                amount1,
                amount0_min,
                amount1_min,
                deadline,
            )
        )
        transaction = function_call.build_transaction(
            {
                "chainId": self.w3.eth.chain_id,
                "from": self.client.address,
                "nonce": self.w3.eth.get_transaction_count(self.client.address),
            }
        )
        return transaction

    def _get_decrease_liquidity_tx(
        self,
        token_id: int,
        liquidity: int,
        amount0_min: int,
        amount1_min: int,
        deadline: int = 2**64,
        wait=False,
    ) -> TxParams:
        """Decrease liquidity

        For Decrease liquidity params refer: https://github.com/Uniswap/v3-periphery/blob/main/contracts/interfaces/INonfungiblePositionManager.sol#L139
        """  # noqa
        function_call = self.functions.decreaseLiquidity(
            (
                token_id,
                liquidity,
                amount0_min,
                amount1_min,
                deadline,
            )
        )
        transaction = function_call.build_transaction(
            {
                "chainId": self.w3.eth.chain_id,
                "from": self.client.address,
                "nonce": self.w3.eth.get_transaction_count(self.client.address),
            }
        )
        return transaction

    def _get_collect_tx(
        self,
        token_id: int,
        recipient: ChecksumAddress = None,
        amount0_max: int = MAX_UINT_128,
        amount1_max: int = MAX_UINT_128,
        wait=False,
    ) -> TxParams:
        """Collect

        For Collect params refer: https://github.com/Uniswap/v3-periphery/blob/main/contracts/interfaces/INonfungiblePositionManager.sol#L160
        """  # noqa
        function_call = self.functions.collect(
            (
                token_id,
                recipient if recipient else self.client.address,
                amount0_max,
                amount1_max,
            )
        )
        transaction = function_call.build_transaction(
            {
                "chainId": self.w3.eth.chain_id,
                "from": self.client.address,
                "nonce": self.w3.eth.get_transaction_count(self.client.address),
            }
        )
        return transaction

    def _create_position(
        self,
        pool_data: PoolData,
        current_tick: int,
        current_price_x96: int,
        lower_tick: int,
        upper_tick: int,
        amount0: int = None,
        amount1: int = None,
    ) -> UncheckedNftPositionRaw:
        if not amount0 and not amount1:
            raise ValueError
        lower_tick = normalize_tick_by_spacing(
            lower_tick, pool_data.immutables.tickSpacing
        )
        upper_tick = normalize_tick_by_spacing(
            upper_tick, pool_data.immutables.tickSpacing
        )
        lower_price_x96 = get_sqrt_ratio_at_tick(lower_tick)
        upper_price_x96 = get_sqrt_ratio_at_tick(upper_tick)
        if amount0:
            amount1 = get_amount1_from_tick_range(
                p=current_price_x96,
                pa=lower_price_x96,
                pb=upper_price_x96,
                amount0=amount0,
            )
            amount0 = get_amount0_from_tick_range(
                p=current_price_x96,
                pa=lower_price_x96,
                pb=upper_price_x96,
                amount1=amount1,
            )
        elif amount1:
            amount0 = get_amount0_from_tick_range(
                p=current_price_x96,
                pa=lower_price_x96,
                pb=upper_price_x96,
                amount1=amount1,
            )
        return UncheckedNftPositionRaw(
            pool=pool_data,
            current_tick=current_tick,
            current_price_x96=current_price_x96,
            lower_tick=lower_tick,
            upper_tick=upper_tick,
            amount0=amount0,
            amount1=amount1,
        )

    def create_position(
        self,
        pool_data: PoolData,
        current_price: float,
        lower_price: float,
        upper_price: float,
        amount0: float = None,
        amount1: float = None,
    ) -> UncheckedNftPosition:
        """
        Create an unChecked liquidity position.
        One of a amount0 or amount1 must be provided.

        Parameters
        ----------
        pool : uniswap.v3.models.PoolData
            current state of the liquidity pool
        current_price : float
            Current price in the liquidity pool
        lower_price : float
            Lower price to be provided in the liquidity pool
        upper_price : float
            Upper price to be provided in the liquidity pool
        amount0 : float
            [Optional] Desired amount token0 to be provided
        amount1 : float
            [Optional] Desired amount token1 to be provided

        Returns
        -------
        uniswap.v3.models.UncheckedNftPosition
            Position to be submitted via self.mint method
        """
        if not amount0 and not amount1:
            raise ValueError

        # Calculate Raw data

        unchecked_nft_position_raw = self._create_position(
            pool_data=pool_data,
            current_tick=pool_data.state.tick,
            current_price_x96=pool_data.state.sqrtPriceX96,
            lower_tick=get_tick_from_price(lower_price),
            upper_tick=get_tick_from_price(upper_price),
            amount0=int(amount0 * (10**pool_data.token0.decimals))
            if amount0 is not None
            else None,
            amount1=int(amount1 * (10**pool_data.token1.decimals))
            if amount1 is not None
            else None,
        )
        if amount0:
            amount1HR = get_amount1_from_price_range(
                p=current_price,
                pa=lower_price,
                pb=upper_price,
                amount0=amount0,
            )
            amount0HR = amount0
        elif amount1:
            amount0HR = get_amount0_from_price_range(
                p=current_price,
                pa=lower_price,
                pb=upper_price,
                amount1=amount1,
            )
            amount1HR = amount1
        amount0 = int(amount0HR * 10**pool_data.token0.decimals)
        amount1 = int(amount1HR * 10**pool_data.token1.decimals)
        return UncheckedNftPosition(
            raw=unchecked_nft_position_raw,
            lower_price=lower_price,
            upper_price=upper_price,
            amount0=amount0,
            amount1=amount1,
            amount0HR=amount0HR,
            amount1HR=amount1HR,
            token0=pool_data.token0,
            token1=pool_data.token1,
            fee=pool_data.immutables.fee,
            adj_amount0=unchecked_nft_position_raw.amount0,
            adj_amount1=unchecked_nft_position_raw.amount1,
            adj_amount0HR=unchecked_nft_position_raw.amount0
            / (10**pool_data.token0.decimals),
            adj_amount1HR=unchecked_nft_position_raw.amount1
            / (10**pool_data.token1.decimals),
            adj_lower_price=round(1.0001**unchecked_nft_position_raw.lower_tick, 18),
            adj_upper_price=round(1.0001**unchecked_nft_position_raw.upper_tick, 18),
        )

    def mint(
        self,
        unchecked_nft_position: UncheckedNftPosition,
        recipient: ChecksumAddress = None,
        deadline: int = 2**64,
        wait: bool = False,
    ) -> HexBytes:
        """
        Mint position for Humans. Please provide result of `self.create_position`.

        Parameters
        ----------
        unchecked_nft_position : UncheckedNftPosition
            prepared data for minting of a new position
        recipient: ChecksumAddress
            Address of the recipient's wallet. By default same wallet.
        deadline: epoch
            deadline for minting transaction. By default 2 ** 64
        wait: bool
            If `True` execution blocked until transaction will be confirmed.
            By default, `False` we don't wait transaction confirmation.

        Returns
        -------
        HexBytes
            tx_hash of the resulting transaction
        """
        # TODO fix passing recipient, deadline, wait with kwargs
        transaction = self._get_mint_tx(
            unchecked_nft_position.token0.address,
            unchecked_nft_position.token1.address,
            unchecked_nft_position.fee,
            unchecked_nft_position.raw.lower_tick,
            unchecked_nft_position.raw.upper_tick,
            unchecked_nft_position.adj_amount0,
            unchecked_nft_position.adj_amount1,
            amount0_min=0,
            amount1_min=0,
            recipient=recipient,
            deadline=deadline,
            wait=wait,
        )
        tx_hash = self.send_tx(self.sign_tx(transaction))
        return tx_hash

    def increase_liquidity(
        self,
        token_id: int,
        unchecked_nft_position: UncheckedNftPosition,
        deadline: int = 2**64,
        wait: bool = False,
    ) -> HexBytes:
        """
        Increase liquidity for the existing position for Humans.
        Please provide result of `self.create_position`.

        Parameters
        ----------
        token_id : int
            ID of the existing position to be top up with a liquidity
        unchecked_nft_position : UncheckedNftPosition
            prepared data for minting of a new position
        deadline: epoch
            deadline for minting transaction. By default 2 ** 64
        wait: bool
            If `True` execution blocked until transaction will be confirmed.
            By default, `False` we don't wait transaction confirmation.

        Returns
        -------
        HexBytes
            tx_hash of the resulting transaction
        """
        # TODO fix passing recipient, deadline, wait with kwargs
        transaction = self._get_increase_liquidity_tx(
            token_id=token_id,
            amount0=unchecked_nft_position.adj_amount0,
            amount1=unchecked_nft_position.adj_amount1,
            amount0_min=0,
            amount1_min=0,
            deadline=deadline,
            wait=wait,
        )
        tx_hash = self.send_tx(self.sign_tx(transaction))
        return tx_hash

    def decrease_liquidity(
        self,
        token_id: int,
        pool: Pool,  # TODO: not pool needed for mint and decrease. I do not like this
        percent: float,
        deadline: int = 2**64,
        wait: bool = False,
        nft_position: NftPosition = None,
    ) -> HexBytes:
        """
        !!! Please use `decrease_collect`, if you want the same behavior
        as on app.uniswap.org
        Decrease liquidity for the existing position for Humans.
        Please provide result of `self.create_position`.

        Parameters
        ----------
        token_id : int
            ID of the existing position to be top up with a liquidity
        pool: Pool
            Current poll of the position
        percent : float
            percent of liquidity will be withdrawn. 0.5 = 50%
        deadline: epoch
            deadline for minting transaction. By default 2 ** 64
        wait: bool
            If `True` execution blocked until transaction will be confirmed.
            By default, `False` we don't wait transaction confirmation.
        nft_position : NftPosition
            [Optional] Current NftPosition

        Returns
        -------
        HexBytes
            tx_hash of the resulting transaction
        """
        if not nft_position:
            nft_position_raw = self._fetch_position_info(token_id=token_id)
            nft_position = self._get_position(
                token_id=token_id, position_raw=nft_position_raw, pool=pool
            )
        else:
            assert nft_position.token_id == token_id

        liquidity = nft_position.raw.liquidity
        withdraw_liquidity = int(liquidity * percent)
        transaction = self._get_decrease_liquidity_tx(
            token_id=token_id,
            liquidity=withdraw_liquidity,
            amount0_min=0,
            amount1_min=0,
            deadline=deadline,
            wait=wait,
        )
        tx_hash = self.send_tx(self.sign_tx(transaction))
        return tx_hash

    def collect(
        self,
        token_id: int,
        recipient: ChecksumAddress = None,
        wait: bool = False,
    ) -> HexBytes:
        """
        Collect fees and all results of single `decrease_liquidity`.

        Parameters
        ----------
        token_id : int
            ID of the existing position to be top up with a liquidity
        recipient: ChecksumAddress
            Address of the recipient's wallet. By default same wallet.
        wait: bool
            If `True` execution blocked until transaction will be confirmed.
            By default, `False` we don't wait transaction confirmation.

        Returns
        -------
        HexBytes
            tx_hash of the resulting transaction
        """
        transaction = self._get_collect_tx(
            token_id=token_id,
            recipient=recipient,
            amount0_max=MAX_UINT_128,
            amount1_max=MAX_UINT_128,
            wait=wait,
        )
        tx_hash = self.send_tx(self.sign_tx(transaction))
        return tx_hash

    def decrease_collect(
        self,
        token_id: int,
        pool: Pool,  # TODO: not pool needed for mint and decrease. I do not like this
        percent: float,
        recipient: ChecksumAddress = None,
        deadline: int = 2**64,
        wait: bool = False,
        nft_position: NftPosition = None,
    ) -> HexBytes:
        """
        Collect fees and all results of single `decrease_liquidity`.

        Parameters
        ----------
        token_id : int
            ID of the existing position to be top up with a liquidity
        pool: Pool
            Current poll of the position
        percent : float
            percent of liquidity will be withdrawn. 0.5 = 50%
        recipient: ChecksumAddress
            [Optional] Address of the recipient's wallet. By default same wallet.
        deadline: epoch
            [Optional] deadline for minting transaction. By default 2 ** 64
        wait: bool
            [Optional] If `True` execution blocked until transaction will be confirmed.
            By default, `False` we don't wait transaction confirmation.
        nft_position : NftPosition
            [Optional] Current NftPosition

        Returns
        -------
        HexBytes
            tx_hash of the resulting transaction
        """
        if not nft_position:
            nft_position_raw = self._fetch_position_info(token_id=token_id)
            nft_position = self._get_position(
                token_id=token_id, position_raw=nft_position_raw, pool=pool
            )
        else:
            assert nft_position.token_id == token_id

        liquidity = nft_position.raw.liquidity
        withdraw_liquidity = int(liquidity * percent)
        transaction_decrease = self._get_decrease_liquidity_tx(
            token_id=token_id,
            liquidity=withdraw_liquidity,
            amount0_min=0,
            amount1_min=0,
            deadline=deadline,
            wait=wait,
        )

        transaction_collect = self._get_collect_tx(
            token_id=token_id,
            recipient=recipient,
            amount0_max=MAX_UINT_128,
            amount1_max=MAX_UINT_128,
            wait=wait,
        )
        multicall_input = (
            transaction_decrease["data"],
            transaction_collect["data"],
        )
        function_call = self.functions.multicall(multicall_input)
        transaction = function_call.build_transaction(
            {
                "chainId": self.w3.eth.chain_id,
                "from": self.client.address,
                "nonce": self.w3.eth.get_transaction_count(self.client.address),
            }
        )

        tx_hash = self.send_tx(self.sign_tx(transaction))
        return tx_hash

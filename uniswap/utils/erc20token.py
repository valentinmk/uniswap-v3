from functools import lru_cache

from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from uniswap.EtherClient.web3_client import EtherClient
from web3.types import TxReceipt

from ..v3.base import BaseContract
from ..v3.models import Token


class EIP20Contract(BaseContract):
    """
    ERC20 contract wrapper.
    Please refer official documentation:
    https://ethereum.org/en/developers/docs/standards/tokens/erc-20/

    Parameters
    ----------
    client : EtherClient
        EtherClient Client
    address : ChecksumAddress
        Address of the ERC20 token smart contract
    abi_path : str
        [Optional] Path to json with ABI of the ERC20 token contract. By default is
        `../utils/abis/eip20.abi.json`
    """

    @lru_cache
    def __init__(
        self,
        client: EtherClient,
        address: ChecksumAddress,
        abi_path: str = "../utils/abis/eip20.abi.json",
    ) -> None:
        super().__init__(client.w3, address, abi_path)
        self.client: EtherClient = client
        self._data = None

    def _get_data(self):
        return Token(
            chainId=self.w3.eth.chain_id,
            decimals=self.functions.decimals().call(),
            symbol=self.functions.symbol().call(),
            name=self.functions.name().call(),
            isNative=False,
            isToken=True,
            address=self.address,
        )

    def allowance(self, contract_address: ChecksumAddress) -> float:
        return (
            self.functions.allowance(self.client.address, contract_address).call()
            / 10**self.data.decimals
        )

    def is_allowance_enough(self, contract_address: ChecksumAddress, amount) -> bool:
        return self.allowance(contract_address) >= amount

    def approve(
        self, contract_address: ChecksumAddress, amount: float, wait=False, force=False
    ) -> HexBytes | TxReceipt | None:
        """
        Send transaction to approve this token with `contract_address` for an `amount`.

        Parameters
        ----------
        contract_address : ChecksumAddress
            EtherClient Client
        amount : float
            Amount to be allowed in human readable format.
        wait : bool
            [Optional]. If true, execution will be locked until transaction not been
            verified by blockchain.
            By default is False.
        force : bool
            [Optional]. If true, will submit approve transaction in anyway.
            If false, will check current allowance and if it is less then requested,
            then submit a transaction.
            By default is False.
        """
        # TODO. It is not good to return diff results
        if self.is_allowance_enough(contract_address, amount) and not force:
            # TODO. It must be an INFO logging message
            print(
                f"""This is no need to approve {contract_address} """
                f"""with {self.data.symbol}. You have allowance enough. """
                """You could override this with a `force` option."""
            )
            return None
        amount_in_wei = int(amount * 10**self.data.decimals)
        function_call = self.functions.approve(contract_address, amount_in_wei)
        transaction = function_call.build_transaction(
            {
                "chainId": self.w3.eth.chain_id,
                "from": self.client.address,
                "nonce": self.w3.eth.get_transaction_count(self.client.address),
            }
        )
        private_key = self.w3.eth.account.decrypt(
            self.client._keyfile_json, self.client._wallet_pass
        )
        signed_tx = self.client.w3.eth.account.sign_transaction(
            transaction, private_key
        )
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        if wait:
            return self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_hash

    @property
    def data(self) -> Token:
        """Get immutable data"""
        if self._data is None:
            self._data = self._get_data()
        return self._data

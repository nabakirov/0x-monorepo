"""Generated wrapper for ERC20Token Solidity contract."""

from typing import Optional, Tuple, Union

from hexbytes import HexBytes
from web3.datastructures import AttributeDict
from web3.providers.base import BaseProvider

from zero_ex.contract_artifacts import abi_by_name

from ._base_contract_wrapper import BaseContractWrapper
from .tx_params import TxParams


class ERC20Token(BaseContractWrapper):
    """Wrapper class for ERC20Token Solidity contract."""

    def __init__(
        self,
        provider: BaseProvider,
        account_address: str = None,
        private_key: str = None,
    ):
        """Get an instance of wrapper for smart contract.

        :param provider: instance of :class:`web3.providers.base.BaseProvider`
        """
        super(ERC20Token, self).__init__(
            provider=provider,
            account_address=account_address,
            private_key=private_key,
        )

    def _ERC20Token(self, token_address):
        """Get an instance of the smart contract at a specific address.

        :returns: contract object
        """
        return self._contract_instance(
            address=token_address, abi=abi_by_name("ERC20Token")
        )

    def approve(
        self,
        token_address: str,
        _spender: str,
        _value: int,
        tx_params: Optional[TxParams] = None,
        view_only: bool = False,
    ) -> Union[HexBytes, bytes]:
        """`msg.sender` approves `_spender` to spend `_value` tokens

        :param _spender: The address of the account able to transfer the tokens
        :param _value: The amount of wei to be approved for transfer
        :param tx_params: transaction parameters
        :param view_only: whether to use transact() or call()

        :returns: transaction hash
        """
        token_address = self._validate_and_checksum_address(token_address)
        _spender = self._validate_and_checksum_address(_spender)
        # safeguard against fractional inputs
        _value = int(_value)

        func = self._ERC20Token(token_address).functions.approve(
            _spender, _value
        )
        return self._invoke_function_call(
            func=func, tx_params=tx_params, view_only=view_only
        )

    def totalSupply(self, token_address: str) -> int:
        """Query total supply of token

        :returns: Total supply of token
        """
        token_address = self._validate_and_checksum_address(token_address)

        func = self._ERC20Token(token_address).functions.totalSupply()
        return self._invoke_function_call(
            func=func, tx_params=None, view_only=True
        )

    def transferFrom(
        self,
        token_address: str,
        _from: str,
        _to: str,
        _value: int,
        tx_params: Optional[TxParams] = None,
        view_only: bool = False,
    ) -> Union[HexBytes, bytes]:
        """send `value` token to `to` from `from` on the condition it is approved by `from`

        :param _from: The address of the sender
        :param _to: The address of the recipient
        :param _value: The amount of token to be transferred
        :param tx_params: transaction parameters
        :param view_only: whether to use transact() or call()

        :returns: transaction hash
        """
        token_address = self._validate_and_checksum_address(token_address)
        _from = self._validate_and_checksum_address(_from)
        _to = self._validate_and_checksum_address(_to)
        # safeguard against fractional inputs
        _value = int(_value)

        func = self._ERC20Token(token_address).functions.transferFrom(
            _from, _to, _value
        )
        return self._invoke_function_call(
            func=func, tx_params=tx_params, view_only=view_only
        )

    def balanceOf(self, token_address: str, _owner: str) -> int:
        """Query the balance of owner

        :param _owner: The address from which the balance will be retrieved
        :returns: Balance of owner
        """
        token_address = self._validate_and_checksum_address(token_address)
        _owner = self._validate_and_checksum_address(_owner)

        func = self._ERC20Token(token_address).functions.balanceOf(_owner)
        return self._invoke_function_call(
            func=func, tx_params=None, view_only=True
        )

    def transfer(
        self,
        token_address: str,
        _to: str,
        _value: int,
        tx_params: Optional[TxParams] = None,
        view_only: bool = False,
    ) -> Union[HexBytes, bytes]:
        """send `value` token to `to` from `msg.sender`

        :param _to: The address of the recipient
        :param _value: The amount of token to be transferred
        :param tx_params: transaction parameters
        :param view_only: whether to use transact() or call()

        :returns: transaction hash
        """
        token_address = self._validate_and_checksum_address(token_address)
        _to = self._validate_and_checksum_address(_to)
        # safeguard against fractional inputs
        _value = int(_value)

        func = self._ERC20Token(token_address).functions.transfer(_to, _value)
        return self._invoke_function_call(
            func=func, tx_params=tx_params, view_only=view_only
        )

    def allowance(self, token_address: str, _owner: str, _spender: str) -> int:
        """Contract method `allowance`.

        :param _owner: The address of the account owning tokens
        :param _spender: The address of the account able to transfer the tokens
        :returns: Amount of remaining tokens allowed to spent
        """
        token_address = self._validate_and_checksum_address(token_address)
        _owner = self._validate_and_checksum_address(_owner)
        _spender = self._validate_and_checksum_address(_spender)

        func = self._ERC20Token(token_address).functions.allowance(
            _owner, _spender
        )
        return self._invoke_function_call(
            func=func, tx_params=None, view_only=True
        )

from dataclasses import dataclass
from typing import Dict, Any, Optional

from libs.py_okx_async.models import ReprWithoutData, StateName, AccountType, AccountTypes


class Currency(ReprWithoutData):
    """
    An instance of a currency.

    Attributes:
        data (Dict[str, Any]): the raw data.
        canDep (bool): the availability to deposit from chain. false: not available, true: available.
        canInternal (bool): the availability to internal transfer. false: not available, true: available.
        canWd (bool): the availability to withdraw to chain. false: not available, true: available.
        token_symbol (str): token symbol, e.g. BTC.
        chain (str): chain name, e.g. USDT-ERC20, USDT-TRC20.
        depQuotaFixed (Optional[str]): the fixed deposit limit, unit in USD. Return empty string if there is no
            deposit limit.
        depQuoteDailyLayer2 (Optional[float]): the layer2 network daily deposit limit.
        logoLink (str): the logo link of currency.
        mainNet (bool): if current chain is main net then return true, otherwise return false.
        maxFee (float): the maximum withdrawal fee for normal address.
        maxFeeForCtAddr (float): the maximum withdrawal fee for contract address.
        maxWd (float): the maximum amount of currency withdrawal in a single transaction.
        minDep (float): the minimum deposit amount of the currency in a single transaction.
        minDepArrivalConfirm (int): the minimum number of blockchain confirmations to acknowledge fund deposit.
            The account is credited after that, but the deposit can not be withdrawn.
        minFee (float): the minimum withdrawal fee for normal address.
        minFeeForCtAddr (float): the minimum withdrawal fee for contract address.
        minWd (float): the minimum withdrawal amount of the currency in a single transaction.
        minWdUnlockConfirm (int): the minimum number of blockchain confirmations required for withdrawal of a deposit.
        name (str): name of currency. There is no related name when it is not shown.
        needTag	(bool):	whether tag/memo information is required for withdrawal.
        usedDepQuotaFixed (Optional[str]): the used amount of fixed deposit quota, unit in USD. Return empty string
            if there is no deposit limit.
        usedWdQuota (float): the amount of currency withdrawal used in the past 24 hours, unit in USD.
        wdQuota (float): the withdrawal limit in the past 24 hours, unit in USD.
        wdTickSz (int): the withdrawal precision, indicating the number of digits after the decimal point.
            The withdrawal fee precision kept the same as withdrawal precision. The accuracy of internal transfer
            withdrawal is 8 decimal places.

    """

    def __init__(self, data: Dict[str, Any]) -> None:
        """
        Initialize the class.

        Args:
            data (Dict[str, Any]): the dictionary with a currency data.

        """
        self.data: Dict[str, Any] = data
        self.canDep: bool = data.get('canDep')
        self.canInternal: bool = data.get('canInternal')
        self.canWd: bool = data.get('canWd')
        self.token_symbol: str = data.get('ccy')
        self.chain: str = '-'.join(data.get('chain').split('-')[1:])
        self.depQuotaFixed: Optional[str] = data.get('depQuotaFixed')
        self.depQuotaFixed = self.depQuotaFixed if self.depQuotaFixed else None
        self.depQuoteDailyLayer2: Optional[float] = data.get('depQuoteDailyLayer2')
        self.depQuoteDailyLayer2 = float(self.depQuoteDailyLayer2) if self.depQuoteDailyLayer2 else None
        self.logoLink: str = data.get('logoLink')
        self.mainNet: bool = data.get('mainNet')
        self.maxFee: float = float(data.get('maxFee'))
        self.maxFeeForCtAddr: float = float(data.get('maxFeeForCtAddr'))
        self.maxWd: float = float(data.get('maxWd'))
        self.minDep: float = float(data.get('minDep'))
        self.minDepArrivalConfirm: int = int(data.get('minDepArrivalConfirm'))
        self.minFee: float = float(data.get('minFee'))
        self.minFeeForCtAddr: float = float(data.get('minFeeForCtAddr'))
        self.minWd: float = float(data.get('minWd'))
        self.minWdUnlockConfirm: int = int(data.get('minWdUnlockConfirm'))
        self.name: str = data.get('name')
        self.needTag: bool = data.get('needTag')
        self.usedDepQuotaFixed: Optional[str] = data.get('usedDepQuotaFixed')
        self.usedDepQuotaFixed = self.usedDepQuotaFixed if self.usedDepQuotaFixed else None
        self.usedWdQuota: float = float(data.get('usedWdQuota'))
        self.wdQuota: float = float(data.get('wdQuota'))
        self.wdTickSz: int = int(data.get('wdTickSz'))


@dataclass
class TransactionType(StateName):
    """
    An instance of a deposit/withdrawal type.
    """
    pass


class TransactionTypes:
    """
    An instance with all deposit/withdrawal types.
    """
    Internal = TransactionType(state='3', name='internal')
    OnChain = TransactionType(state='4', name='on-chain')


@dataclass
class DepositStatus(StateName):
    """
    An instance of a deposit status.
    """
    pass


class DepositStatuses:
    """
    An instance with all deposit statuses.
    """
    WaitingForConfirmation = DepositStatus(state='0', name='waiting for confirmation')
    Credited = DepositStatus(state='1', name='deposit credited')
    Successful = DepositStatus(state='2', name='deposit successful')
    Pending = DepositStatus(state='8', name='pending due to temporary deposit suspension on this crypto currency')
    BlacklistedAddress = DepositStatus(state='11', name='match the address blacklist')
    Frozen = DepositStatus(state='12', name='account or deposit is frozen')
    Subaccount = DepositStatus(state='13', name='sub-account deposit interception')
    KYCLimit = DepositStatus(state='14', name='KYC limit')

    statuses_dict = {
        '0': WaitingForConfirmation,
        '1': Credited,
        '2': Successful,
        '8': Pending,
        '11': BlacklistedAddress,
        '12': Frozen,
        '13': Subaccount,
        '14': KYCLimit
    }


class Deposit(ReprWithoutData):
    """
    An instance of a withdrawal.

    Attributes:
        data (Dict[str, Any]): the raw data.
        token_symbol (str): token symbol, e.g. BTC.
        chain (str): chain name, e.g. USDT-ERC20, USDT-TRC20.
        amt (float): deposit amount.
        from_ (str): deposite account. If the deposit comes from an internal transfer, this field displays
            the account information of the internal transfer initiator, which can be mobile phone number,
            email address, account name, and will return "" in other cases.
        areaCodeFrom (str): if from is a phone number, this parameter return area code of the phone number.
        to_ (str): deposit address. If the deposit comes from the on-chain, this field displays the on-chain address,
            and will return "" in other cases.
        txId (str): hash record of the deposit.
        ts (int): time that the deposit is credited, Unix timestamp format in milliseconds, e.g. 1655251200000.
        state (Optional[DepositStatus]): status of deposit.
        depId (int): deposit ID.
        fromWdId (int): internal transfer initiator's withdrawal ID. If the deposit comes from internal transfer,
            this field displays the withdrawal ID of the internal transfer initiator, and will return "" in other cases.
        actualDepBlkConfirm (int): actual amount of blockchain confirm in a single deposit.

    """

    def __init__(self, data: Dict[str, Any]) -> None:
        """
        Initialize the class.

        Args:
            data (Dict[str, Any]): the dictionary with a deposit data.

        """
        self.data: Dict[str, Any] = data
        self.token_symbol: str = data.get('ccy')
        self.chain: str = '-'.join(data.get('chain').split('-')[1:])
        self.amt: float = float(data.get('amt'))
        self.from_: str = data.get('from')
        self.areaCodeFrom: str = data.get('areaCodeFrom')
        self.to_: str = data.get('to')
        self.txId: str = data.get('txId')
        self.ts: int = data.get('ts')
        self.ts = int(int(self.ts) / 1000) if self.ts else 0
        self.state: Optional[DepositStatus] = DepositStatuses.statuses_dict.get(data.get('state'))
        self.depId: int = int(data.get('depId'))
        self.fromWdId: Optional[int] = data.get('fromWdId')
        self.fromWdId = int(self.fromWdId) if self.fromWdId else None
        self.actualDepBlkConfirm: int = int(data.get('actualDepBlkConfirm'))


@dataclass
class WithdrawalStatus(StateName):
    """
    An instance of a withdrawal status.
    """
    pass


class WithdrawalStatuses:
    """
    An instance with all withdrawal statuses.
    """
    Canceling = WithdrawalStatus(state='-3', name='canceling')
    Canceled = WithdrawalStatus(state='-2', name='canceled')
    Failed = WithdrawalStatus(state='-1', name='failed')
    WaitingWithdrawal = WithdrawalStatus(state='0', name='waiting withdrawal')
    Withdrawing = WithdrawalStatus(state='1', name='withdrawing')
    WithdrawSuccess = WithdrawalStatus(state='2', name='withdraw success')
    WaitingMannualReview4 = WithdrawalStatus(state='4', name='waiting mannual review')
    WaitingMannualReview5 = WithdrawalStatus(state='5', name='waiting mannual review')
    WaitingMannualReview6 = WithdrawalStatus(state='6', name='waiting mannual review')
    Approved = WithdrawalStatus(state='7', name='approved')
    WaitingMannualReview8 = WithdrawalStatus(state='8', name='waiting mannual review')
    WaitingMannualReview9 = WithdrawalStatus(state='9', name='waiting mannual review')
    WaitingTransfer = WithdrawalStatus(state='10', name='waiting transfer')
    WaitingMannualReview12 = WithdrawalStatus(state='12', name='waiting mannual review')

    statuses_dict = {
        '-3': Canceling,
        '-2': Canceled,
        '-1': Failed,
        '0': WaitingWithdrawal,
        '1': Withdrawing,
        '2': WithdrawSuccess,
        '4': WaitingMannualReview4,
        '5': WaitingMannualReview5,
        '6': WaitingMannualReview6,
        '7': Approved,
        '8': WaitingMannualReview8,
        '9': WaitingMannualReview9,
        '10': WaitingTransfer,
        '12': WaitingMannualReview12
    }


class Withdrawal(ReprWithoutData):
    """
    An instance of a withdrawal.

    Attributes:
        data (Dict[str, Any]): the raw data.
        chain (str): chain name, e.g. USDT-ERC20, USDT-TRC20.
        fee (float): withdrawal fee amount.
        token_symbol (str): token symbol, e.g. BTC.
        clientId (int): client-supplied ID.
        amt (float): withdrawal amount.
        txId (str): hash record of the withdrawal. This parameter will returned "" for internal transfers.
        from_ (str): withdrawal account. It can be email/phone.
        areaCodeFrom (str): area code for the phone number. If from is a phone number, this parameter returns
            the area code for the phone number.
        to_ (str): receiving address.
        areaCodeTo (str): area code for the phone number. If to is a phone number, this parameter returns
            the area code for the phone number.
        state (Optional[WithdrawalStatus]): status of withdrawal.
        ts (int): time the withdrawal request was submitted, Unix timestamp format in milliseconds, e.g. 1655251200000.
        wdId (int): withdrawal ID.
        nonTradableAsset (Optional[bool]): whether it is a non-tradable asset or not true: non-tradable asset,
            false: tradable asset.
        tag (Optional[str]): some currencies require a tag for withdrawals. This is not returned if not required.
        pmtId (Optional[str]): some currencies require a payment ID for withdrawals. This is not returned
            if not required.
        memo (Optional[str]): some currencies require this parameter for withdrawals. This is not returned
            if not required.
        addrEx (Optional[str]): withdrawal address attachment (This will not be returned if the currency
            does not require this) e.g. TONCOIN attached tag name is comment, the return will be {'comment':'123456'}.
        feeCcy (Optional[str]): withdrawal fee currency, e.g. USDT.

    """

    def __init__(self, data: Dict[str, Any]) -> None:
        """
        Initialize the class.

        Args:
            data (Dict[str, Any]): the dictionary with a withdrawal data.

        """
        self.data: Dict[str, Any] = data
        self.chain: str = '-'.join(data.get('chain').split('-')[1:])
        self.fee: float = float(data.get('fee'))
        self.token_symbol: str = data.get('ccy')
        self.clientId: Optional[int] = data.get('clientId')
        self.clientId = int(self.clientId) if self.clientId else None
        self.amt: float = float(data.get('amt'))
        self.txId: str = data.get('txId')
        self.from_: str = data.get('from')
        self.areaCodeFrom: str = data.get('areaCodeFrom')
        self.to_: str = data.get('to')
        self.areaCodeTo: str = data.get('areaCodeTo')
        self.state: Optional[WithdrawalStatus] = WithdrawalStatuses.statuses_dict.get(data.get('state'))
        self.ts: int = data.get('ts')
        self.ts = int(int(self.ts) / 1000) if self.ts else 0
        self.wdId: int = int(data.get('wdId'))
        self.nonTradableAsset: Optional[bool] = data.get('nonTradableAsset')
        self.tag: Optional[str] = data.get('tag')
        self.pmtId: Optional[str] = data.get('pmtId')
        self.memo: Optional[str] = data.get('memo')
        self.addrEx: Optional[str] = data.get('addrEx')
        self.feeCcy: Optional[str] = data.get('feeCcy')


class WithdrawalToken(ReprWithoutData):
    """
    An instance of a withdrawal token.

    Attributes:
        data (Dict[str, Any]): the raw data.
        amt (float): withdrawal amount.
        wdId (int): withdrawal ID.
        token_symbol (str): token symbol, e.g. BTC.
        clientId (Optional[int]): client-supplied ID.
        chain (str): chain name, e.g. USDT-ERC20, USDT-TRC20. A combination of case-sensitive alphanumerics,
            all numbers, or all letters of up to 32 characters.

    """

    def __init__(self, data: Dict[str, Any]) -> None:
        """
        Initialize the class.

        Args:
            data (Dict[str, Any]): the dictionary with a withdrawal token data.

        """
        self.data: Dict[str, Any] = data
        self.amt: float = float(data.get('amt'))
        self.wdId: int = int(data.get('wdId'))
        self.token_symbol: str = data.get('ccy')
        self.clientId: Optional[int] = data.get('clientId')
        self.clientId = int(self.clientId) if self.clientId else None
        self.chain: str = '-'.join(data.get('chain').split('-')[1:])


@dataclass
class TransferType(StateName):
    """
    An instance of a transfer type.
    """
    pass


class TransferTypes:
    """
    An instance with all transfer types.
    """
    WithinAccount = TransferType(state='0', name='within account')
    MasterToSub = TransferType(state='1', name='master to sub')
    SubToMasterMasterKey = TransferType(state='2', name='sub to master master key')
    SubToMasterSubKey = TransferType(state='3', name='sub to master sub key')
    SubToSub = TransferType(state='4', name='sub to sub')

    statuses_dict = {
        '0': WithinAccount,
        '1': MasterToSub,
        '2': SubToMasterMasterKey,
        '3': SubToMasterSubKey,
        '4': SubToSub
    }


class Transfer(ReprWithoutData):
    """
    An instance of a transfer.

    Attributes:
        data (Dict[str, Any]): the raw data.
        transId (int): transfer ID.
        clientId (Optional[int]): client-supplied ID.
        token_symbol (str): token symbol, e.g. BTC.
        from_ (AccountType): the remitting account.
        amt (float): transfer amount.
        to_ (AccountType): the beneficiary account.

    """

    def __init__(self, data: Dict[str, Any]) -> None:
        """
        Initialize the class.

        Args:
            data (Dict[str, Any]): the dictionary with a transfer data.

        """
        self.data: Dict[str, Any] = data
        self.transId: int = int(data.get('transId'))
        self.clientId: Optional[int] = data.get('clientId')
        self.clientId = int(self.clientId) if self.clientId else None
        self.token_symbol: str = data.get('ccy')
        self.from_: AccountType = AccountTypes.types_dict.get(data.get('from'))
        self.amt: float = float(data.get('amt'))
        self.to_: AccountType = AccountTypes.types_dict.get(data.get('to'))

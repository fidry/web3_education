from dataclasses import dataclass

from libs.py_okx_async.models import ReprWithoutData, StateName


@dataclass
class SubaccountType(StateName):
    """
    An instance of a sub-account type.
    """
    pass


class SubaccountTypes:
    """
    An instance with all sub-account types.
    """
    Standard = SubaccountType(state='1', name='standard')
    ManagedTrading = SubaccountType(state='2', name='managed trading')
    Custody = SubaccountType(state='5', name='custody')

    types_dict = {
        '1': Standard,
        '2': ManagedTrading,
        '5': Custody
    }


class SubaccountInfo(ReprWithoutData):
    """
    An instance of a sub-account.

    Attributes:
        data (Dict[str, Any]): the raw data.
        enable (bool): sub-account status. true: Normal false: Frozen.
        subAcct (str): sub-account name.
        type (Optional[SubaccountTypes]): sub-account type.
        label (str): sub-account note.
        mobile (Optional[str]): mobile number that linked with the sub-account.
        gAuth (bool): if the sub-account switches on the Google Authenticator for login authentication.
            true: On false: Off.
        canTransOut (bool): whether the sub-account has the right to transfer out. true: can transfer out,
            false: cannot transfer out.
        ts (int): sub-account creation time, Unix timestamp in millisecond format. e.g. 1597026383085.

    """

    def __init__(self, data: dict[str, ...]) -> None:
        """
        Initialize the class.

        Args:
            data (Dict[str, Any]): the dictionary with a sub-account data.

        """
        self.data: dict[str, ...] = data
        self.enable: bool = data.get('enable')
        self.subAcct: str = data.get('subAcct')
        self.type: SubaccountTypes | None = SubaccountTypes.types_dict.get(data.get('type'))
        self.label: str = data.get('label')
        self.mobile: str | None = data.get('mobile')
        self.gAuth: bool = data.get('gAuth')
        self.canTransOut: bool = data.get('canTransOut')
        self.ts: int = data.get('ts')
        self.ts = int(int(self.ts) / 1000) if self.ts else 0

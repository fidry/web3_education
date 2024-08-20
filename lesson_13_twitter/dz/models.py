from pydantic import BaseModel, RootModel


class AccountInfo(BaseModel):
    password: str
    mail: str
    auth_token: str
    totp: str


class Accounts(RootModel[dict[str, AccountInfo]]):
    pass

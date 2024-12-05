import asyncio

from py_okx_async.OKXClient import OKXClient

from data.config import okx_credentials
from okx.okx_actions import OKXActions
from py_okx_async.models import OKXCredentials, Chains, AccountTypes


async def main():
    okx_client = OKXClient(credentials=okx_credentials)

    # subaccounts_lst = await okx_client.subaccount.list()
    # for subaccount_name in subaccounts_lst:
    #     print(subaccount_name)
    #     print(await okx_client.subaccount.asset_balances(subAcct=subaccount_name, token_symbol='ETH'))
    # print()

    # print(await okx_client.asset.currencies(token_symbol='ETH'))
    # currencies = await okx_client.asset.currencies()
    # for currency in currencies:
    #     print(currency, currencies[currency])
    # print()

    # withdrawal_history = await okx_client.asset.withdrawal_history()
    # print(withdrawal_history)
    # for withdrawal in list(withdrawal_history)[:3]:
    #     print(withdrawal, withdrawal_history[withdrawal])
    # print()

    # ------------------------------------------------------------------------------------------------

    okx_actions = OKXActions(credentials=okx_credentials)

    # print(await okx_actions.all_balances_are_zero(amount=1))
    # print(await okx_actions.get_withdrawal_fee(token_symbol='ETH', chain=Chains.ArbitrumOne))
    # print(await okx_actions.try_to_get_tx_hash(wd_id=115902399))


if __name__ == '__main__':
    if okx_credentials.completely_filled():
        asyncio.run(main())
    else:
        print('Specify all variables in the .env file!')

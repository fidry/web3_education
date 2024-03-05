import asyncio

from client import AptosClient
from data import config
from data.models import Tokens, TokenAmount

from tasks.liquidswap import Liquidswap
from tasks.pancakeswap import PancakeSwap
from tasks.domain_names import DomainNames

from tasks.controller import Controller


async def example():
    '''
    docs: https://aptos.dev/tutorials/
    examples: https://github.com/aptos-labs/aptos-core/tree/main/ecosystem/python/sdk/examples
    '''
    client = AptosClient(private_key=config.private_key, proxy=config.proxy)
    print(client.address)

    # print(client.get_coin_data(token=Tokens.LZ_USDT))
    # print(client.get_decimals(token=Tokens.APT))
    # print(client.get_balance(token=Tokens.APT))

    # tokens = client.get_sorted_token_balance_dict()
    # for token in tokens:
    #     print(f'name: {token.name}; balance: {tokens[token].Ether}')

    # print(client.get_token_price(
    #     amount_in=TokenAmount(amount=1.88, decimals=6),
    #     from_token=Tokens.APT,
    #     to_token=Tokens.LZ_USDT
    # ).Ether)

    # print(client.get_wallet_balance_in_apt().Ether)
    # print(client.get_account_domain_names())

    # print(len(client.get_tx_list()))
    # print(client.get_tx_info(version='278070315'))

    # liquidswap = Liquidswap(aptos_client=client)
    # amount_apt = TokenAmount(0.2, decimals=8)
    # print(liquidswap.swap(from_token=Tokens.APT, to_token=Tokens.LZ_USDC, amount_in=amount_apt))
    # print(liquidswap.swap(from_token=Tokens.LZ_USDT, to_token=Tokens.LZ_WETH))

    controller = Controller(aptos_client=client)
    # domain_names = controller.aptos_client.get_account_domain_names()
    # print(domain_names)

    # dn = DomainNames(aptos_client=client)
    # print(dn.mint_domain_name())

    '''
    1) написать функцию стейка ликвидности на ditto
    2) написать функцию стейка ликвидности на tortuga
    3) написать функцию для подсчета транзакций на добавление ликвидности
    '''

    amount_apt = TokenAmount(0.2, decimals=8)
    # print(controller.ditto.stake(amount_in=amount_apt))
    # print(controller.tortuga.stake(amount_in=amount_apt))
    print(controller.liquidswap.swap(from_token=Tokens.LP_TORTUGA, to_token=Tokens.APT))
    print(controller.liquidswap.swap(from_token=Tokens.LP_DITTO, to_token=Tokens.APT))
    # print(controller.count_stakes())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(example())

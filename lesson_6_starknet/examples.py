import asyncio
import time

from starknet_py.contract import Contract

from client import StarknetClient
from data import config, models


async def main():
    client = StarknetClient(
        private_key=config.private_key,
        account_address=config.account_address,
    )

    # -----------------------------------------------------------------------------     get block info
    print(await client.starknet_client.get_block(block_number=1))

    # -----------------------------------------------------------------------------     account address
    print('account address int:', client.account.address)
    print('account address hex:', hex(client.account.address))

    # -----------------------------------------------------------------------------     get_balance example

    print('eht_balance:', (await client.get_balance(token_address=models.ETH_ADDRESS)).Ether)
    print('dai_balance:', (await client.get_balance(token_address=models.DAI_ADDRESS)).Ether)

    # -----------------------------------------------------------------------------     call example
    usdc_contract = Contract(
        address=models.USDC_ADDRESS,
        abi=models.DEFAULT_TOKEN_ABI,
        provider=client.account
    )

    info = await usdc_contract.functions['decimals'].call()
    print('USDC decimals:', StarknetClient.get_data(info))

    eth_contract = await Contract.from_address(
        address=models.ETH_ADDRESS,
        provider=client.account,
        proxy_config=False
    )
    print(eth_contract.data.abi)

    info = await eth_contract.functions['decimals'].call()
    print('ETH decimals:', StarknetClient.get_data(info))

    # get symbol
    info = await usdc_contract.functions['symbol'].call()
    print('symbol:', StarknetClient.get_text_from_decimal(info=info))


if __name__ == '__main__':
    asyncio.run(main())

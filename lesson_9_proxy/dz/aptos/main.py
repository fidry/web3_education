import asyncio

from aptos_sdk.account_address import AccountAddress

from aptos.client import AptosClient
from aptos.data import models


async def main():
    address = '0x34b4ec1694e54bbc85db45479794ca6e37be40bb60b57de6a51b0b899910caea'
    pk = '0x9234e0f1d1ec0455255434a22df1d311173b9121d75dfac24f076b8b78830e28'
    proxy = 'http://amcTW8cm:PM3EESuL@154.194.103.215:64632'

    client = AptosClient(private_key=pk, proxy=proxy)

    token = models.Tokens.LZ_USDC

    token_address = AccountAddress.from_hex(
        token.address.split('::')[0]
    )

    # coin_info = client.account_resource(
    #     account_address=token_address, resource_type=f'{models.ResourceType.info}<{token.address}>')
    # print(coin_info)

    coin_info = await client.account_resource_async(
        account_address=token_address, resource_type=f'{models.ResourceType.info}<{token.address}>')
    print(coin_info)


if __name__ == '__main__':
    asyncio.run(main())

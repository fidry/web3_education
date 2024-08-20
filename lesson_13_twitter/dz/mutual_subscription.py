import json
import asyncio
import random

import twitter
from loguru import logger

from utils import text_to_json
from models import Accounts


accounts_path = '../0b4a82.txt'
accounts_json_path = './accounts.json'
proxy = 'СЮДА НАДО ВСТАВИТЬ ПРОКСИ'

# text_to_json(from_path=accounts_path, to_path=accounts_json_path)

with open(accounts_json_path) as f:
    accounts_json = json.load(f)

accounts = Accounts.parse_obj(accounts_json).root

logins = list(accounts.keys())
# print(logins)
# print(accounts['TysonColli37825'])


async def main():
    for login in logins:
        account = accounts[login]

        twitter_account = twitter.Account(
            auth_token=account.auth_token,
            password=account.password,
            email=account.mail,
            totp_secret=account.totp
        )

        async with twitter.Client(twitter_account, proxy=proxy) as twitter_client:
            logger.info(f"Logged in as @{twitter_account.username} (id={twitter_account.id})")

            for to_subscribe_login in logins:
                to_subscribe_account = await twitter_client.request_user_by_username(username=to_subscribe_login)
                if to_subscribe_account.id == twitter_account.id:
                    continue

                if await twitter_client.follow(user_id=to_subscribe_account.id):
                    logger.success(f'{twitter_account.username} successfully subscribed to '
                                   f'{to_subscribe_account.username}')
                else:
                    logger.error(f'{twitter_account.username} subscription error to '
                                 f'{to_subscribe_account.username}')
                    logger.error('dsfm')


if __name__ == '__main__':
    asyncio.run(main())

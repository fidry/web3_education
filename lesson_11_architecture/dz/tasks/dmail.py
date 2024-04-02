"""
https://era.zksync.network/tx/0x3c0e0fd9fd832647c31520fe95c70d22b95246630cc01c5f163675327c6b6219
https://era.zksync.network/tx/0x713ea9757009702af0156716c443e3cf9c824aadea07258e8e4e048d480a4f26
"""

import hashlib

from faker import Faker
from loguru import logger
from web3.types import TxParams


from tasks.base import Base
from libs.eth_async.data.models import TxArgs
from data.models import Contracts


class Dmail(Base):
    async def send_dmail(self):
        email_address, theme_info = Dmail.fake_acc()

        logger.info(f'Sending e-mail to: {email_address} theme: {theme_info} - via Dmail')
        failed_text = f'Failed send e-mail via Dmail'

        to = await Dmail.sha256(email_address)
        theme = await Dmail.sha256(theme_info)

        contract = await self.client.contracts.get(contract_address=Contracts.DMAIL)

        params = TxArgs(
            email=to,
            theme=theme,
        )

        tx_params = TxParams(
            to=contract.address,
            data=contract.encodeABI('send_mail', args=params.tuple()),
        )

        tx = await self.client.transactions.sign_and_send(tx_params=tx_params)
        receipt = await tx.wait_for_receipt(client=self.client, timeout=300)

        if receipt:
            return f'E-mail was sent to {email_address} via Dmail: TX-Hash {tx.hash.hex()}'
        return f'{failed_text}!'

    @staticmethod
    def fake_acc():
        fake = Faker()
        profile = fake.profile()
        email_address, theme = profile['mail'], fake.company()

        return email_address, theme

    @staticmethod
    async def sha256(data):
        sha256_hash = hashlib.sha256()
        sha256_hash.update(data.encode('utf-8'))
        hash_str = sha256_hash.hexdigest()

        return hash_str

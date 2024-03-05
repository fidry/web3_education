import requests
import random

from aptos_sdk.transactions import (
    EntryFunction,
    TransactionPayload,
    TransactionArgument
)
from aptos_sdk.bcs import Serializer

from tasks.base import Base
from data.models import DomainNamesInfo
from utils.utils import get_explorer_hash_link


class DomainNames(Base):
    @staticmethod
    def get_random_usernames():
        url = 'https://spinxo.com/services/NameService.asmx/GetNames'
        payload = {
            "snr": {
                "category": 0,
                "UserName": "",
                "Hobbies": "",
                "ThingsILike": "",
                "Numbers": "",
                "WhatAreYouLike": "",
                "Words": "",
                "Stub": "username",
                "LanguageCode": "en",
                "NamesLanguageID": "45",
                "Rhyming": False,
                "OneWord": False,
                "UseExactWords": False,
                "ScreenNameStyleString": "Any",
                "GenderAny": False,
                "GenderMale": False,
                "GenderFemale": False
            }
        }
        r = requests.post(url, json=payload)
        names = r.json()['d']['Names']
        return names

    def get_available_name(self):
        names = DomainNames.get_random_usernames()
        while True:
            if not names:
                return self.get_available_name()

            name = names.pop(random.randint(0, len(names) - 1)).lower()

            if len(name) < 6:
                continue

            url = f'https://www.aptosnames.com/api/mainnet/v1/address/{name}'

            if self.aptos_client.proxy:
                r = requests.get(url, proxies={"https": f"http://{self.aptos_client.proxy}"})
            else:
                r = requests.get(url)
            if r.text == "{}":
                return name

    def register_domain(self, nickname: str) -> str:
        failed_text = f'Failed to register domain tx'
        try:
            self.aptos_client.client_config.max_gas_amount += 5000

            # https://github.com/aptos-labs/aptos-core/blob/main/ecosystem/python/sdk/examples/multisig.py
            modules_serializer = Serializer.sequence_serializer(Serializer.to_bytes)

            payload = EntryFunction.natural(
                DomainNamesInfo.AptosNames.script,
                DomainNamesInfo.AptosNames.function,
                [],
                [
                    TransactionArgument(nickname, Serializer.str),
                    TransactionArgument(31536000, Serializer.u64),
                    TransactionArgument([], modules_serializer),
                    TransactionArgument([], modules_serializer),
                ],
            )

            signed_transaction = self.aptos_client.create_bcs_signed_transaction(
                self.aptos_client.signer, TransactionPayload(payload))
            tx = self.aptos_client.submit_bcs_transaction(signed_transaction)
            self.aptos_client.wait_for_transaction(tx)
            return f'Claimed "{nickname}" domain: {get_explorer_hash_link(tx)}'

        except Exception as e:
            if 'out of gas' in str(e).lower():
                self.aptos_client.client_config.max_gas_amount += random.randint(4500, 6500)
                return f'{failed_text}: Gas less than minimum: {e}'
            elif "EINVALID_PROOF_OF_KNOWLEDGE" in str(e):
                return f'{failed_text}: Invalid proof of knowledge while try to register domain. ' \
                       f'Skip this wallet and get another: {e}'

            elif "INSUFFICIENT_BALANCE_FOR_TRANSACTION_FEE" in str(e):
                return f'{failed_text}: insufficient balance for transaction fee: {e}'
            return f'{failed_text}: Something went wrong: {e}'

    def mint_domain_name(self) -> str:
        failed_text = f'Failed mint domain name'
        apt_balance = self.aptos_client.get_balance()
        if apt_balance.Ether < 1.002:
            return f'{failed_text}: To low APT balance ({apt_balance.Ether})'
        try:
            nickname = self.get_available_name()
            return self.register_domain(nickname=nickname)
        except Exception as e:
            return f'{failed_text}: something went wrong: {e}'
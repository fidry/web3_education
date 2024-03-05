from client import AptosClient


class Base:
    def __init__(self, aptos_client: AptosClient):
        self.aptos_client = aptos_client

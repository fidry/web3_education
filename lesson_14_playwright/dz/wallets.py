from data.models import Wallets


WALLETS = Wallets.parse_obj([
    {
        'address': '',
        'private_key': '',
    },
]).root

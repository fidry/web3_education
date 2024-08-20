import json


def text_to_json(from_path: str, to_path: str) -> None:
    res_dict = {}
    with open(from_path) as f:
        accounts = f.read().split('\n\n')

    login = ''
    for account in accounts:
        for row in account.split('\n'):
            if not row:
                continue
            value = row.strip().split(': ')[1]
            if row.startswith('login'):
                login = value
                res_dict[login] = {}
            elif row.startswith('password'):
                res_dict[login]['password'] = value
            elif row.startswith('mail'):
                res_dict[login]['mail'] = value
            elif row.startswith('passwordmail'):
                res_dict[login]['passwordmail'] = value
            elif row.startswith('AUTH_TOKEN'):
                res_dict[login]['auth_token'] = value
            elif row.startswith('2fa'):
                res_dict[login]['totp'] = value

    with open(to_path, 'w') as f:
        json.dump(res_dict, f)


if __name__ == '__main__':
    accounts_path = '../0b4a82.txt'
    accounts_json_path = './accounts.json'
    text_to_json(accounts_path, accounts_json_path)

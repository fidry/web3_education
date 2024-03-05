import requests


def change_mobile_ip(change_ip_url: str) -> bool:
    try:
        response = requests.get(change_ip_url)
        print(response.text)
        if 'success' not in response.text:
            return False
        return True
    except Exception as e:
        return False


proxies = {
    'http': 'http://228e532527:2e25236787@92.255.251.69:40962',
    'https': 'http://228e532527:2e25236787@92.255.251.69:40962'
}


your_ip = requests.get(
    'http://eth0.me/', proxies=proxies, timeout=10
).text.rstrip()

print(your_ip)

change_ip_url = ('https://proxys.io/ru/api/v2/change-mobile-proxy-ip'
                 '?key=10be37368e08eee1b2f2ccca5d012762'
                 '&order=21569'
                 '&proxy=1'
                 )


print(
    change_mobile_ip(change_ip_url=change_ip_url)
)

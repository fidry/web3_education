import requests


# pip install -U 'requests[socks]'
proxies = {
    'http': 'socks5://amcTW8cm:PM3EESuL@154.194.103.215:64633',
    'https': 'socks5://amcTW8cm:PM3EESuL@154.194.103.215:64633'
}
# protocol://login:passwd@host:port

your_ip = requests.get(
    'http://eth0.me/', proxies=proxies, timeout=10
).text.rstrip()

print(your_ip)

import requests


proxies = {
    'http': 'http://amcTW8cm:PM3EESuL@154.194.103.215:64632',
    'https': 'http://amcTW8cm:PM3EESuL@154.194.103.215:64632'
}

# protocol://login:passwd@host:port

your_ip = requests.get(
    'http://eth0.me/', proxies=proxies, timeout=10
).text.rstrip()

print(your_ip)

async def format_proxy(proxy: str) -> dict:
    username_password, server_port = proxy.replace('http://', '').split('@')
    username, password = username_password.split(':')
    server, port = server_port.split(':')
    proxy = {
        "server": f"http://{server}:{port}",
        "username": username,
        "password": password,
    }
    return proxy

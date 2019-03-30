from kazoo.client import KazooClient
zk = KazooClient(hosts="106.12.222.49:2181")
zk.start()
print(zk.state)
zk.ensure_path("/sg/city")
if not zk.exists("/sg/city/beijing"):
    zk.create("/sg/city/beijing", b"this is h_tg node111.",ephemeral = True)

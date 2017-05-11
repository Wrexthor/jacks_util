# import paramiko
from sshtunnel import SSHTunnelForwarder
import os, click
from time import sleep

@click.command()
@click.option('--ip', '-i', help="Remote server ip")
@click.option('--port', '-p', default=443,  help="Remote server port")
@click.option('--user', '-u', default='',  help="Username")
@click.option('--key', '-k', help="Private key path")
@click.option('--password', '-p', help="Private key password")
@click.option('--rbindaddress', '-ra', default='127.0.0.1', help="Private key password")
@click.option('--rbindport', '-rp', default=3389, help="Private key password")


def start_rdp():
    os.startfile('C:\Windows\system32\mstsc.exe /v:127.0.0.1:3390')


def main(ip, port, user, key, password, rbindaddress, rbindport):
    REMOTE_SERVER_IP = ip
    REMOTE_SERVER_PORT = port
    USERNAME = user
    PRIVATE_KEY = key
    PRIVATE_KEY_PASSWORD = password
    # PRIVATE_SERVER_IP = '2.2.2.2'
    REMOTE_BIND_ADDRESS = rbindaddress
    REMOTE_BIND_PORT = rbindport

    with SSHTunnelForwarder(
        (REMOTE_SERVER_IP, REMOTE_SERVER_PORT),
        ssh_username=USERNAME,
        ssh_pkey=PRIVATE_KEY,
        ssh_private_key_password=PRIVATE_KEY_PASSWORD,
        remote_bind_address=(REMOTE_BIND_ADDRESS, REMOTE_BIND_PORT),
        local_bind_address=('127.0.0.1', 3390)
    ) as tunnel:
        print(tunnel.local_bind_port)
        start_rdp()
        while True:
            sleep(1)


if __name__ == '__main__':
    main()
'''
# v1

with SSHTunnelForwarder(
    (REMOTE_SERVER_IP, REMOTE_SERVER_PORT),
    ssh_username="",
    ssh_pkey="/var/ssh/rsa_key",
    ssh_private_key_password="secret",
    remote_bind_address=(PRIVATE_SERVER_IP, 22),
    local_bind_address=('0.0.0.0', 10022)
) as tunnel:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('127.0.0.1', 10022)
    # do some operations with client session
    client.close()

print('FINISH!')

# v2

server = SSHTunnelForwarder(
    #'pahaz.urfuclub.ru',
    (REMOTE_SERVER_IP, REMOTE_SERVER_PORT),
    ssh_username=USERNAME,
    ssh_pkey=PRIVATE_KEY,
    ssh_private_key_password=PRIVATE_KEY_PASSWORD,
    remote_bind_address=(REMOTE_BIND_ADDRESS, REMOTE_BIND_PORT)
)

server.start()

print(server.local_bind_port)  # show assigned local port
# work with `SECRET SERVICE` through `server.local_bind_port`.

server.stop()
'''
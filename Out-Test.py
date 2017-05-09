import outcp, click

@click.command()
@click.option('--port', '-p', multiple=True, help="Port to test, can be multiple")
@click.option('--address', '-a', default='portquiz.net',
              help="Address to attempt connection to, needs to listen to "
                   "specified port, defaults to portquiz.net")


def main(port, address):
    # test = []
    for item in port:
        test = outcp.test(int(item), address)
        if test != -1:
            click.echo("{} replied on port {}".format(address, port))
        else:
            click.echo("{} failed to connect on port {}".format(address, port))
        # test.append(outcp.test(port, address))


if __name__ == '__main__':
    main()

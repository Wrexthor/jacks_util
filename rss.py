import click
import feedparser
import pickle
import os.path
import time


@click.command()
@click.option('--address', '-a', multiple=True, help="Add address of site to store, can be multiple sites \n"
                                                     "Example: -a google.com -a bing.com")
@click.option('--list', '-l', is_flag=True, default=False, help="Lists current addresses stored")
@click.option('--remove', '-r', help="Remove address from store")
@click.option('--live', '-L', is_flag=True, default=False, help="Keeps alive, waiting for new "
                                                                "feed items and writing them")
@click.option('--match', '-m', default=None, help="Get all news matching keyword in title")
@click.option('--print', '-p', is_flag=True, default=False, help="Prints news to screen")


# main function calling other functions
def rss(address, list, remove, live, match, print):

    if remove:
        write_address(remove_item(remove))
    if list:
        print_list(open_address())
    if address:
        add_address(address)
    news = parse(open_address())
    if print:
        print_news(news, match)
    while live:
        click.echo('Going live!')
        # check if new news have been added
        old_news = news
        news = parse(open_address())
        diff = list(set(old_news) - set(news))
        if diff:
            click.echo('Diff is true')  # debug
            print_news(diff, match)
        else:
            click.echo('Diff is false')  # debug
        click.echo('Sleeping 5')  # debug
        time.sleep(5)


def remove_item(remove):
    address = open_address()
    if remove in address:
        return address.remove(remove)
    else:
        click.echo('Address to be removed not found')


def print_list(address):
    for line in address:
        click.echo(line)


def print_news(news, match):
    if match:
        # search for matching word in list of lists of news
        for site in news:
            for item in site.entries:
                if match in item.title:
                    click.echo("{} \n {}".format(item.title, item.link))
    else:
        for site in news:
            for item in site.entries:
                click.echo("{} \n {}".format(item.title, item.link))


# writes list of addresses to address.list file
def add_address(address):
    new_address = [(open_address()).append(address)]
    with open('address.list', 'wb') as handle:
        pickle.dump(new_address, handle, protocol=pickle.HIGHEST_PROTOCOL)


def write_address(address):
    new_address = list(address)
    with open('address.list', 'wb') as handle:
        pickle.dump(new_address, handle, protocol=pickle.HIGHEST_PROTOCOL)


# used to open address.list file
def open_address():
    if os.path.isfile('address.list'):
        with open('address.list', 'rb') as handle:
            return pickle.load(handle)
    else:
        empty = []
        with open('address.list', 'wb') as handle:
            pickle.dump(empty, handle, protocol=pickle.HIGHEST_PROTOCOL)

        with open('address.list', 'rb') as handle:
            return pickle.load(handle)


def parse(urls):
    parsed = []
    for url in urls:
        parsed.append(feedparser.parse(url))
    return parsed


if __name__ == '__main__':
    rss()
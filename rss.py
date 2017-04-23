import click
import feedparser
import os.path
import time
import json

@click.command()
@click.option('--address', '-a', multiple=True, help="Add address of site to store, can be multiple sites \n"
                                                     "Example: -a google.com -a bing.com")
@click.option('--list', '-l', is_flag=True, default=False, help="Lists current addresses stored")
@click.option('--remove', '-r', help="Remove address from store")
@click.option('--live', '-L', is_flag=True, default=False, help="Keeps alive, waiting for new "
                                                                "feed items and writing them")
@click.option('--match', '-m', default=None, help="Get all news matching keyword in title")
@click.option('--print', '-p', is_flag=True, default=False, help="Prints news to screen")
@click.option('--clear', '-c', is_flag=True, default=False, help="Removes all saved addresses")


# main function calling other functions
def rss(address, list, remove, live, match, print, clear):

    if clear:
        if os.path.isfile('address.txt'):
            os.remove('address.txt')
            click.echo('Addresses cleared')
        else:
            click.echo('Error attempting to clear addresses, no previous addresses found to clear.')

    if remove:
        write_address(remove_item(remove))
    if list:
        print_list(open_address())
    if address:
        add_address(address)
    if print:
        news = parse(open_address())
        print_news(news, match)
    # pre-parse news for later comparison in while loop
    if live:
        news = parse(open_address())
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
    if address:
        if remove in address:
            return address.remove(remove)
        else:
            click.echo('Address to be removed not found')
    else:
        click.echo('Error attempting to delete address; no addresses found')


def print_list(address):
    if address:
        for line in address:
            click.echo(line)
    else:
        click.echo('Error attempting to list addresses; no addresses found')


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
    # convert address to list
    address = list(address)
    # check if values are stored in file from before
    if open_address():
        # get old values, add new ones
        click.echo('Address found in add address, appending and writing to file')  # debug
        # debug stuff below
        click.echo('Returned type from open address is list:')
        click.echo(type(open_address()))
        click.echo(open_address())
        click.echo(type(address))
        # debug stuff above
        old = open_address()
        new_address = old + address
        #new_address = [(open_address()).append(address)]
        # write old + new to file
        with open('address.txt', 'w') as handle:
            json.dump(new_address, handle)
            # pickle.dump(new_address, handle, protocol=pickle.HIGHEST_PROTOCOL)
    # write values directly to file
    else:
        click.echo('No Address found in write address, writing to file')  # debug
        write_address(address)


def write_address(address):
    # convert address to list to prevent
    # problems with tuples when adding new data
    if address:
        click.echo('Address found in write address, writing to file')  # debug
        new_address = list(address)
        with open('address.txt', 'w') as handle:
            json.dump(new_address, handle)
            # pickle.dump(new_address, handle, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        click.echo('Error attempting to write address to file; no address found')


# used to open address.list file
def open_address():
    # check if file exist
    if os.path.isfile('address.txt'):
        click.echo('File found, opening')  # debug
        # if it does, open it
        with open('address.txt', 'r') as handle:
            return json.load(handle)
            # return list(pickle.load(handle))
    # no file exists, can't open file
    else:
        click.echo('No file found, opening file failed')  # debug
        return None


def parse(urls):
    if urls:
        parsed = []
        for url in urls:
            parsed.append(feedparser.parse(url))
        return parsed
    else:
        click.echo('Error attempting to parse URLs, no URLs found')


if __name__ == '__main__':
    rss()
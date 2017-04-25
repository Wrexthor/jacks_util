import click
import feedparser
import os.path
# import time
import json

@click.command()
@click.option('--address', '-a', multiple=True, help="Add address of site to store, can be multiple sites \n"
                                                     "Example: -a google.com -a bing.com")
@click.option('--list', '-l', is_flag=True, default=False, help="Lists current addresses stored")
@click.option('--remove', '-r', help="Remove address from store")
#@click.option('--live', '-L', is_flag=True, default=False, help="Keeps alive, waiting for new " # i give up, no one uses etag/modified
#                                                                "feed items and writing them")
@click.option('--match', '-m', default=None, help="Get all news matching keyword in title")
@click.option('--print', '-p', is_flag=True, default=False, help="Prints news to screen")
@click.option('--clear', '-c', is_flag=True, default=False, help="Removes all saved addresses")


# main function calling other functions
def rss(address, list, remove, match, print, clear):

    if clear:
        if os.path.isfile('address.txt'):
            os.remove('address.txt')
            click.echo('Addresses cleared')
        else:
            click.echo('Error attempting to clear addresses, no previous addresses found to clear.')

    if remove:
        # check that remove function returns value
        #write_address(remove_item(remove))
        r = remove_item(remove)
        if r:
            # write value to file
            write_address(r)
        else:
            os.remove('address.txt')
            #click.echo('Error attempting to write addresses after removal; addresses not found')

    if list:
        print_list(open_address())
    if address:
        add_address(address)
    if print:
        news = parse(open_address())
        print_news(news, match)
    '''
    this whole feature is on hold until i can come up with a 
    good way to get only the newest items from feed

    # pre-parse news for later comparison in while loop
    if live:
        click.echo('Live is {}'.format(live))  # debug
        news = parse(open_address())


    i = 0
    while live:
        news = parse(open_address())
        for item in news:
            check_update(item, item.href)
        # click.echo('Going live!')  # debug
        # check if new news have been added
        #new_news = parse(open_address())
        # diff = list(set(new_news) - set(news))
        #diff = set(new_news) - set(news)

        #diff = get_difference(new_news, news)
        #diff = set(new_news).difference(set(news))
        # click.echo(diff)

        if i == 0:
            old_news = print_news(news, match)
        
        if diff:
            click.echo('Diff is true')  # debug
            print_news(diff, match)
        else:
            click.echo('Diff is false')  # debug
        
        # click.echo(type(diff))
        
        click.echo(i)
        if i > 0:
            click.echo('I is greater than 1!')
            diff = list(set(news) - set(new_news))
            list(set(news) - set(new_news))
            click.echo('Diff: {}'.format(diff))  # debug
            if diff:
                click.echo('Diff is true')  # debug
                print_news(diff, match)
            else:
                click.echo('Diff is false')  # debug
        
        #news = parse(open_address())
        click.echo('Sleeping 5 minutes')  # debug
        time.sleep(300)
        i += 1
'''

def get_difference(list1, list2):
    s = set(list2)
    list3 = [x for x in list1 if x not in s]
    return list(list3)

def check_update(old_feed, address):
    # store the etag and modified
    last_etag = old_feed.etag
    last_modified = old_feed.modified
    # check if new version exists
    feed_update = feedparser.parse(address, etag=last_etag, modified=last_modified)
    # return based on result
    if feed_update.status == 304:
        return False
    else:
        return True


def remove_item(remove):
    address = open_address()
    if address:
        try:
            address.remove(remove)
            click.echo('Removed {}'.format(remove))
            return address
        except ValueError:
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
    click.echo('\n\n')
    result = []
    if match:
        # search for matching word in list of lists of news
        for site in news:
            for item in site.entries:
                if match in item.title:
                    click.secho("\n{} \n {}".format(item.title, item.link), fg='yellow')
                    # add to results
                    result.append(item.title)
                    result.append(item.link)
    else:
        for site in news:
            for item in site.entries:
                click.secho("\n{}".format(item.title))
                click.secho("{}".format(item.link), fg='cyan')
                # add to results
                result.append(item.title)
                result.append(item.link)
    click.echo('\n\n')
    return result


# writes list of addresses to address.list file
def add_address(address):
    # convert address to list
    address = list(address)
    # check if values are stored in file from before
    if open_address():
        # get old values, add new ones
        # click.echo('Address found in add address, appending and writing to file')  # debug
        old = open_address()
        new_address = old + address
        #new_address = [(open_address()).append(address)]
        # write old + new to file
        with open('address.txt', 'w') as handle:
            json.dump(new_address, handle)
            # pickle.dump(new_address, handle, protocol=pickle.HIGHEST_PROTOCOL)
    # write values directly to file
    else:
        # click.echo('No Address found in write address, writing to file')  # debug
        write_address(address)


def write_address(address):
    # convert address to list to prevent
    # problems with tuples when adding new data
    if address:
        # click.echo('Address found in write address, writing to file')  # debug
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
        # click.echo('File found, opening')  # debug
        # if it does, open it
        with open('address.txt', 'r') as handle:
            return json.load(handle)
            # return list(pickle.load(handle))
    # no file exists, can't open file
    else:
        # click.echo('No file found, opening file failed')  # debug
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
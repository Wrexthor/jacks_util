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
    if address:
        add_address(address)
    news = parse(open_address())
    if print:
        print_news(news, match)
    while live:
        click.echo('Going live!')
        # check if new news have been added
        if news != parse(open_address()):
            print_news(parse(open_address()), match)
        news = parse(open_address())
        time.sleep(60)



def print_news(news, match):
    '''
    
        any(e[1] in match for e in news)
    '''
    # print = []
    if match != None:
        # search for matching word in list of lists of news
        for site in news:
            for item in site.entries:
                #article = [item.title, item.published, item.link]
                if match in item.title:
                    #print.append(article)
                    click.echo("{} \n {}".format(item.title, item.link))
    else:
        for site in news:
            for item in site.entries:
                click.echo("{} \n {}".format(item.title, item.link))
                # print("{} \n {}".format(item.title, item.link))



# writes list of addresses to address.list file
def add_address(address):
    with open('address.list', 'wb') as handle:
        pickle.dump(address, handle, protocol=pickle.HIGHEST_PROTOCOL)


# used to open address.list file
def open_address():
    #address_list = []
    if os.path.isfile('address.list'):
        with open('address.list', 'rb') as handle:
            #address_list.clear()
            #address_list.append(pickle.load(handle))
            return pickle.load(handle)
            #return address_list
    else:
        click.echo('No previous addresses found, please add some addresses')
        return None


def parse(urls):
    parsed = []
    for url in urls:
        parsed.append(feedparser.parse(url))
    return parsed


if __name__ == '__main__':
    rss()
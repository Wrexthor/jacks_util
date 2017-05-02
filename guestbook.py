import json
import os
import time

class Entry:
    def __init__(self, text, time):
        self.text = text
        self.time = time
    '''    
    def store(self):
        with open('journal.txt', 'w') as handle:
            json.dump(handle)
    '''

def guestbook():
    text = write_entry()
    time = get_date()
    e = Entry(text, time)
    save_data(e)


def write_entry():
    r = input('Enter journal entry:')
    return r

def get_date():
    return time.time()

def save_data(data):
    with open('journal.txt', 'w') as handle:
        json.dump(handle, data)

def open_data():
    if os.path.isfile('journal.txt'):
        with open('journal.txt', 'r') as handle:
            return json.load(handle)

guestbook()
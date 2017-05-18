'''
Monitors file usage and stores last opened files
Possible to search recently used files

Check for existing index file, if none exist, create one, else open it and store in memory
Create event watching for launch file events, run in separate thread
When event found, write name:path of file to index dict, then write to disk file

search function, trying to match input to name in index dict, triggered by tab for auto-completion
return name:path matching input pattern

run function, takes path and starts whatever it is

main()
    while loop with input waiting for user, tab for autocompletion if possible

'''
import wmi
import json
import os
import threading
import pythoncom


def watch(file_path):
    """
    Watches for creation of new processes, stores in index dict and prints index    
    :return:
    """
    pythoncom.CoInitialize()
    index = {}
    c = wmi.WMI()
    watcher = c.watch_for(
        notification_type="Creation",
        wmi_class="Win32_Process",
        delay_secs=1
    )
    while True:
        stuff = watcher()
        os_procs = ('backgroundTaskHost.exe', 'svchost.exe', 'conhost.exe', 'SearchFilterHost.exe', 'python.exe', 'smartscreen.exe', 'SearchProtocolHost.exe')
        # check that it's not a standard OS process
        if stuff.__getattr__('Name') not in os_procs:
            index[stuff.__getattr__('Name')] = stuff.__getattr__('ExecutablePath')
            print(index)
            write_file(file_path, index)
        else:
            print('Standard OS task found and skipped')
            pass

        # print(stuff.__getattr__('Name'))
        # print(stuff.__getattr__('ExecutablePath'))


def write_file(path, data):
    """
    Writes data as json to file
    :param path: 
    :param data: 
    :return: 
    """
    try:
        with open(path, 'w') as handle:
            json.dump(data, handle)
    except Exception as e:
        print(e)


def read_file(path):
    """
    Reads json file and returns content
    :param path: 
    :return: 
    """
    if os.path.isfile(path):
        try:
            with open(path, 'r') as handle:
                return json.load(handle)
        except Exception as e:
            print(e)


def search(text, index):
    """
    Searches content in index for matching string to text
    :param text: 
    :param index: 
    :return: 
    """
    for key, val in index.items():
        if text.upper() in key.upper():
            # print('Found match!')
            return val
    #if text.upper() in index.keys:
     #   print('Found match!')

def main():
    path = 'data.json'
    while True:
        index = read_file(path)
        print(type(index))
        #print(index)
        in_text = input('Start (tab for autocomplete): ')
        if index:
            search(in_text, index)
        else:
            print('Index not ready, no results found!')


processThread = threading.Thread(target=watch, args=('data.json',))  # <- note extra ','
processThread.start()

# t1 = FuncThread(watch, 'data.json')
# t1.start()

if __name__ == '__main__':
    main()
# watch()

'''


c = wmi.WMI ()

#filename = r"c:\temp\temp.txt"
#process = c.Win32_Process
#process_id, result = process.Create (CommandLine="notepad.exe " + filename)
watcher = c.watch_for (
  notification_type="Creation",
  wmi_class="Win32_Process",
  delay_secs=1

)

stuff = watcher()
print(stuff.__getattr__('Name'))
print(stuff.__getattr__('ExecutablePath'))
'''
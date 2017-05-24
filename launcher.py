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

"""
Gets values of registry of recent programs, stores in dict with name:path
Allows user to enter a string that is matched to a name and starts the program
Currently lots of previous ideas in the code that does or does not run
"""
import wmi
import json
import os
import threading
import pythoncom
import winreg
import subprocess
import win32com.client


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


def get_lnk_path(lnk_path):
    """
    Gets the full path that a lnk file points to
    :param lnk_path: 
    :return: string with full path
    """
    try:
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(lnk_path)
        return shortcut.Targetpath
    except Exception as e:
        print(e)
        return None


def get_folder_content(folder_path):
    """
    Gets all files recursivly under given folder path
    :param folder_path: 
    :return: list with full path of each file
    """
    paths = []
    try:
        for root, dirs, files in os.walk(folder_path):
            for name in files:
                paths.append(root + '\\' + name)
        #print(paths)
        return paths
    except Exception as e:
        print(e)
        return None




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
    :return: content of read json file
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
            res = (key, val)
            return res
    #if text.upper() in index.keys:
     #   print('Found match!')





def reg_keys(key_path, hive):
    """
    Reads value of all keys under specified key path    
    :param key_path: 
    :param hive: 
    :return: nested list with with key values
    """
    result = []
    # set reg hive
    if hive == 'HKEY_CURRENT_USER':
        reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    elif hive == 'HKEY_LOCAL_MACHINE':
        reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    elif hive == 'HKEY_CURRENT_CONFIG':
        reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_CONFIG)
    elif hive == 'HKEY_CLASSES_ROOT':
        reg = winreg.ConnectRegistry(None, winreg.HKEY_CLASSES_ROOT)
    elif hive == 'HKEY_USERS':
        reg = winreg.ConnectRegistry(None, winreg.HKEY_USERS)
    else:
        return None
    # open key from path
    key = winreg.OpenKey(reg, key_path)
    # get amount of sub keys
    count = winreg.QueryInfoKey(key)
    # iterate over keys
    for i in range(count[1]):
        # get value of key
        res = winreg.EnumValue(key, i)
        result.append(res)
        # print(res)
    return result


def filter_reg(lists):
    """
    filters the nested list from registry function
    into a dict with 
    key = name of app
    value = path to app
    if app has an .exe/.EXE file ending
    :param lists: 
    :return: dict with name:path
    """
    res = {}
    for a in lists:
        # try if .exe matches
        try:
            # get index of match .exe
            ind = a[0].index('.exe')
        # if not matches, try .EXE
        except ValueError:
            try:
                # get index of match .exe
                ind = a[0].index('.EXE')
                # its probably a dll, set ind to None
            except:
                ind = None
        # if ind is not None, add to result
        if ind:
            # split string from beginning to index + 4 to include .exe
            res[a[1]] = (a[0][:(ind + 4)])
    return res

def start_exe(path):
    """
    opens given exe file as a subprocess
    :param path: path to exe file
    :return: 
    """
    try:
        subprocess.Popen(path)
    except Exception as e:
        print(e)

def main():
    path = 'data.json'

    key_path = r"Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\MuiCache"
    key_hive = 'HKEY_CURRENT_USER'
    '''
    key_values = []
    for key in key_path:
        key_values.append(filter_reg(reg_keys(key, key_hive)))
    '''
    key_values = filter_reg(reg_keys(key_path, key_hive))
    # get userprofile path from env variable
    userprofile = os.environ['USERPROFILE']
    recent_files = []
    startmenu_files = []
    # get content from recents folder
    print('getting recent')
    recent_content = get_folder_content(userprofile + r"\AppData\Roaming\Microsoft\Windows\Recent")
    # get content from startmenu folder
    print('getting startmenu')
    startmenu = get_folder_content(userprofile + r"\AppData\Roaming\Microsoft\Windows\Start Menu\Programs")



    for file in startmenu:
        print('processing startmenu')
        if '.lnk' in file:
            startmenu_files.append(get_lnk_path(file))
    # make sure only last 10 files are processed
    counter = 0

    for file in recent_content:
        print(counter)
        counter = counter + 1
        if counter > 10:
            break
        if '.lnk' in file:
            recent_files.append(get_lnk_path(file))

    #reg1 = filter_reg(reg_keys(key_path, key_hive))
    write_file(path, key_values)
    print(key_values)
    while True:
        '''
        # index = read_file(path)
        # print(type(index))
        # print(index)
        # in_text = input('Start (tab for autocomplete): ')
        if index:
            search(in_text, index)
        else:
            print('Index not ready, no results found!')
        '''
        in_text = input('Start (tab for autocomplete): ')
        if in_text:
            exe_path = search(in_text, key_values)
            in_text = None
            print('Starting {}'.format(exe_path[0]))
            start_exe(exe_path[1])



#processThread = threading.Thread(target=watch, args=('data.json',))  # <- note extra ','
#processThread.start()

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
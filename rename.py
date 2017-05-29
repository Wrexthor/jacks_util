"""
CLI that takes a list of files as input and renames them according to a pattern
"""

import click
import os
import piexif
import time


@click.command()
@click.option('--path', prompt=True, help="Path to folder to run against")
@click.option('--pattern', '-p', help="Name pattern, ie image###.jpg")
#@click.option('--reverse', '-r', default=False, help="Reverse order of renaming")
@click.option('--recurse', '-R', is_flag=True, help="Recursivly renames ALL sub files in folder, please be careful!")
@click.option('--simulate', '-s', is_flag=True, help="Simulates results, writing changes to console without doing anything")
@click.option('--lower', '-l', is_flag=True, help="Make all names lowercase")
@click.option('--upper', '-u', is_flag=True, help="Make all names uppercase")
@click.option('--exif', '-e', is_flag=True, help="Strips exif metadata from JPEG/TIFF images")
@click.option('--date', '-d', is_flag=True, help="Appends datetime to files in format: _%Y/%m/%d_%H:%M")
@click.option('--strip', '-S', help="Use none to remove whitespaces or a character to replace them with")
@click.option('--rename', '-r', help="Use %Y:%m:%d:%H:%M datetime format or ### for incremental number, example newname###")


def main(path, pattern, recurse, exif, simulate, lower, upper, date, strip, rename):
    # get files from path if recurse
    if recurse:
        files = get_files_recurse2(path)
    # else get files only in folder
    else:
        files = get_files2(path)

    # check if reverse true, if so, reverse list
    #if reverse:
    #    files.reverse()

    # check lower option
    if lower and not upper:
        to_lowercase2(files)

    if lower and upper:
        print("You can't use both upper and lower")

    # check upper option
    if upper and not lower:
        to_uppercase2(files)

    # check if strip exif
    if exif:
        print('Stripping metadata:')
        strip_exif2(files)

    if rename:
        print('Renaming based on input:')
        rename_custom(files, rename)

    if date:
        print('Appending date:')
        add_date(files)

    if strip:
        print('Stripping/replacing whitespaces:')
        replace_space(files, strip)

    # if simulate, only print result

        simulate2_(files)
    # else print result and rename
    # check that there is a new name
    if files[0].newname:
        if simulate:
            print('Simulated results:')
        else:
            print('Renaming:')
        rename2_(files, simulate)
    else:
        print('No action take as no new name was given')



class File:
    def __init__(self, oldname, path):
        self.oldname = oldname
        self.newname = None
        self.path = path


def add_date(files):
    now = time.strftime("_%Y/%m/%d_%H:%M")
    for file in files:
        file.newname = (file.oldname.split('.')[0]) + now + '.' + file.oldname.split('.')[1]


def strip_exif2(files):
    """
    Strips EXIF metadata from imagees
    :param files: dict of files with name:path    
    """
    for file in files:
        try:
            if '.jpg' in file.oldname or '.tiff' in file.oldname:
                piexif.remove((file.path + file.oldname))
                print('Metadata removed from {}'.format(file.oldname))
            else:
                print('{} is not a JPEG or TIFF and wont be processed'.format(file.oldname))
        except Exception as e:
            print(e)


def rename_custom(files, rename_):
    # rename.trim('')
    i = 1
    for file in files:
        if '#' in rename_:
            # count number of # present
            count = rename_.count('#')
            # create a variable for the
            replace_ = '#' * count
            # create a variable for use in format based on count
            fill = '0' + str(count) + 'd'
            # add newname to file object
            if '.' in file.oldname:
                file.newname = rename_.replace(replace_, format(i, fill)) + '.' + file.oldname.split('.')[1]
            else:
                file.newname = rename_.replace(replace_, format(i, fill))
            i = i + 1
        if '.' in file.oldname:
            file.newname = rename_ + '.' + file.oldname.split('.')[1]
        else:
            file.newname = rename_
        if '%Y' in rename_:
                try:
                    year = time.strftime("%Y")
                    file.newname = file.newname.replace('%Y', year)
                except:
                    pass
        if '%m' in rename_:
                try:
                    month = time.strftime("%m")
                    file.newname = file.newname.replace('%m', month)
                except:
                    pass
        if '%d' in rename_:
                try:
                    day = time.strftime("%d")
                    file.newname = file.newname.replace('%d', day)
                except:
                    pass
        if '%H' in rename_:
                try:
                    hour = time.strftime("%H")
                    file.newname = file.newname.replace('%H', hour)
                except:
                    pass
        if '%M' in rename_:
                try:
                    minute = time.strftime("%M")
                    file.newname = file.newname.replace('%M', minute)
                except:
                    pass
        i = i + 1


def replace_space(files, char):
    if char == 'none':
        char = ''
    for file in files:
        file.newname = file.oldname.replace(' ', char)


def get_files2(folder_path):
    f = []
    try:
        for (dirpath, dirnames, filenames) in os.walk(folder_path):
            for file in filenames:
                f.append(File(file, (dirpath + os.sep)))
            break
        return f
    except Exception as e:
        print(e)
        return None


def to_uppercase2(files):
    for file in files:
        file.newname = file.oldname.upper()


def to_lowercase2(files):
    for file in files:
        file.newname = file.oldname.lower()


def get_files_recurse2(folder_path):
    paths = []
    try:
        for root, dirs, files in os.walk(folder_path):
            for name in files:
                paths.append(File(name, (root + os.sep)))
        return paths
    except Exception as e:
        print(e)
        return None


def simulate2_(files):
    for file in files:
        print('{} renamed to {}'.format(file.oldname, file.newname))


def rename2_(files, simulate):
    # declare loop variables
    i = 0
    last = None
    exists = None
    for file in files:
        # try to rename
        try:
            # if simulate check if name from last iteration is same as in this one
            if simulate:
                if last:
                    # set variable to True of False
                    exists = file.newname == last
            # if not simulating, rename files, if exists error is thrown
            if not simulate:
                os.rename((file.path + file.oldname), (file.path + file.newname))
            # if filename is same and simulating, throw error manually
            if exists:
                raise WindowsError(17, 'File already exists')
            # if above succeeds, print what happened
            print('{} renamed to {}'.format(file.oldname, file.newname))

        except WindowsError as e:
            # if error is file already exist
            if e.errno == 17:
                # check if file has a file ending
                if '.' in file.newname:
                    # store filending in variable
                    fileending = '.' + file.newname.split('.')[1]
                    # if not simulating, rename
                    if not simulate:
                        # rename using filending, appending 3 digit value based on i
                        os.rename((file.path + file.oldname), (file.path + file.newname.split('.')[0] + '-' + format(i, '02d') + fileending))
                    print('{} renamed to {}'.format(file.oldname, (file.newname.split('.')[0] + '-' + format(i, '02d') + fileending)))
                else:
                    # rename without filending,  appending 3 digit value based on i
                    os.rename((file.path + file.oldname),
                              (file.path + file.newname.split('.')[0] + '-' + format(i, '02d')))
                    print('{} renamed to {}'.format(file.oldname, (file.newname.split('.')[0] + '-' + format(i, '02d'))))
            else:
                # error was not file exists, print it
                print(e.winerror)
        last = file.newname
        i = i + 1



if __name__ == '__main__':
    main()
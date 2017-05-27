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

    if date:
        print('Appending date:')
        add_date(files)

    if strip:
        print('Stripping/replacing whitespaces:')
        replace_space(files, strip)

    # if simulate, only print result
    if simulate:
        print('Simulated results:')
        simulate2_(files)
    # else print result and rename
    else:
        # check that there is a new name
        if files[0].newname:
            print('Renaming:')
            simulate2_(files)
            rename2_(files)
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


def rename_custom(files, rename):
    rename.trim('')
    i = 1
    for file in files:
        if '#' in rename:
            # count number of # present
            count = file.oldname.count('#')
            # create a variable for the
            replace = '#' * count
            # create a variable for use in format based on count
            fill = '0' + str(count) + 'd'
            # add newname to file object
            file.newname = file.oldname.replace(replace, format(i, fill))
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
                paths.append(File(name, (root + "\\")))
        return paths
    except Exception as e:
        print(e)
        return None


def simulate2_(files):
    for file in files:
        print('{} renamed to {}'.format(file.oldname, file.newname))


def rename2_(files):
    for file in files:
        try:
            os.rename((file.path + file.oldname), (file.path + file.newname))
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
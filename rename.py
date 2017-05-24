"""
CLI that takes a list of files as input and renames them according to a pattern
"""

import click
import os
import piexif


@click.command()
@click.option('--path', prompt=True, help="Path to folder to run against")
@click.option('--pattern', '-p', prompt=True, help="Name pattern, ie image###.jpg")
#@click.option('--reverse', '-r', default=False, help="Reverse order of renaming")
@click.option('--recurse', '-R', default=False, help="Recursivly renames ALL sub files in folder, please be careful!")
@click.option('--simulate', '-s', default=False, help="Simulates results, writing changes to console without doing anything")
@click.option('--lower', '-l', default=False, help="Make all names lowercase")
@click.option('--upper', '-u', default=False, help="Make all names uppercase")
@click.option('--exif', '-e', default=False, help="Strips exif metadata from JPEG/TIFF images")

def pattern():
    if pattern == '###':
        print('stuff')
    elif pattern == '':
        print('stuff')
    elif pattern == '###':
        print('stuff')


def strip_exif(files):
    """
    Strips EXIF metadata from imagees
    :param files: dict of files with name:path    
    """
    for key, val in files:
        try:
            if '.jpg' in key or '.tiff' in key:
                piexif.remove(val+key)
                print('Metadata removed from {}'.format(key))
            else:
                print('{} is not a JPEG or TIFF and wont be processed'.format(key))
        except Exception as e:
            print(e)

def get_files(folder_path):
    """
    Gets files in a folder
    :param folder_path: 
    :return: dict with name:fullpath
    """
    f = {}
    try:
        for (dirpath, dirnames, filenames) in os.walk(folder_path):
            #f.extend(dirpath + '\\' + filenames)
            for file in filenames:
                #f.append(dirpath + "\\" + file)
                f[file] = (dirpath + "\\")
            break
        return f
    except Exception as e:
        print(e)
        return None


def to_uppercase(files):
    """
    Change all filenames to uppercase
    :param files: dict with name:path
    :return: dict with(oldname, newname):path
    """
    res = {}
    '''
    for file in files:
        res.append(file.upper)
    return res
    
    for key, val in files:
        key = key.upper
        res[key] = val
    '''
    for key, val in files:
        newkey = (key, key.lower)
        res[newkey] = val
    return res


def to_lowercase(files):
    """
    Change all filenames to lowercase
    :param files: dict with name:path
    :return: dict with(oldname, newname):path
    """
    '''
    res = []
    for file in files:
        res.append(file.lower)
    return res
    '''
    res = {}
    for key, val in files:
        newkey = (key, key.lower)
        res[newkey] = val
    ''''
    for key, val in files:
        key = key.lower
        res[key] = val
    '''
    return res


def get_files_recurse(folder_path):
    """
    Gets all files recursivly under given folder path
    :param folder_path: 
    :return: dict with name:fullpath
    """
    paths = {}
    try:
        for root, dirs, files in os.walk(folder_path):
            for name in files:
                #paths.append(root + '\\' + name)
                paths[name] = (root + '\\')
        return paths
    except Exception as e:
        print(e)
        return None


def numbered(files, pattern):
    for file in files:
        file


def simulate(files):
    for key, val in files:
        print('{} renamed to {}'.format(key[0], key[1]))



def rename(files):
    """
    Renames files from old to new name
    :param files: dict with (olename, newname):path     
    """
    for key, val in files:
        try:
            os.rename((val + key[0]), (val + key[1]))
        except Exception as e:
            print(e)


def main(path, pattern, recurse, exif, simulate, lower, upper):
    # get files from path if recurse
    if recurse:
        files = get_files_recurse(path)
    # else get files only in folder
    else:
        files = get_files(path)

    # check if reverse true, if so, reverse list
    #if reverse:
    #    files.reverse()

    # check lower option
    if lower and not upper:
        result = to_lowercase(files)
    # handle if both are true
    else:
        print("You can't use both upper and lower")

    # check upper option
    if upper and not lower:
        result = to_uppercase(files)
    # handle if both are true
    else:
        print("You can't use both upper and lower")

    # check if strip exif
    if exif:
        print('Stripping metadata;')
        strip_exif(files)

    # add old and new values to a dict
    # order does not matter as new name has already been assigned
    # dictionary = dict(zip(files, result))

    # if simulate, only print result
    if simulate:
        print('Simulated results:')
        simulate(result)
        '''
        for key, val in dictionary:
            simulate(key, val)
        '''
    # else print result and rename
    else:
        print('Renaming:')
        simulate(result)
        rename(result)
        '''
        for key, val in dictionary:
            simulate(key, val)
            rename(key, val)
        '''


if __name__ == '__main__':
    main()
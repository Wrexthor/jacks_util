"""
CLI that takes a list of files as input and renames them according to a pattern
"""

import click
import os

@click.command()
@click.option('--path', prompt=True, help="Path to folder to run against")
@click.option('--pattern', '-p', prompt=True, help="Name pattern, ie image###.jpg")
@click.option('--reverse', '-r', default=False, help="Reverse order of renaming")
@click.option('--recurse', '-R', default=False, help="Recursivly renames ALL sub files in folder, please be careful!")
@click.option('--simulate', '-s', default=False, help="Simulates results, writing changes to console without doing anything")
@click.option('--lower', '-l', default=False, help="Make all names lowercase")
@click.option('--upper', '-u', default=False, help="Make all names uppercase")

def pattern():
    if pattern == '###':
        print('stuff')
    elif pattern == '':
        print('stuff')
    elif pattern == '###':
        print('stuff')


def get_files(folder_path):
    """
    Gets files in a folder
    :param folder_path: 
    :return: returns list with path to files
    """
    f = []
    try:
        for (dirpath, dirnames, filenames) in os.walk(folder_path):
            f.extend(filenames)
            break
        return f
    except Exception as e:
        print(e)
        return None


def to_uppercase(files):
    """
    Change all filenames to uppercase
    :param files: 
    :return: list of filenames
    """
    res = []
    for file in files:
        res.append(file.upper)
    return res


def to_lowercase(files):
    """
    Change all filenames to lowercase
    :param files: 
    :return: list of filenames
    """
    res = []
    for file in files:
        res.append(file.lower)
    return res


def get_files_recurse(folder_path):
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
        return paths
    except Exception as e:
        print(e)
        return None


def numbered(files, pattern):
    for file in files:
        file


def simulate(oldname, newname):
    """
    Print old and new name
    :param oldname: 
    :param newname:    
    """
    print('{} renamed to {}'.format(oldname, newname))



def rename(oldname, newname):
    """
    Renames file from old to new
    :param oldname: 
    :param newname:    
    """
    try:
        os.rename(oldname, newname)
    except Exception as e:
        print(e)


def main(path, pattern, recurse, reverse, simulate, lower, upper):
    # get files from path if recurse
    if recurse:
        files = get_files_recurse(path)
    # else get files only in folder
    else:
        files = get_files(path)

    # check if reverse true, if so, reverse list
    if reverse:
        files.reverse()

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

    # add old and new values to a dict
    # order does not matter as new name has already been assigned
    dictionary = dict(zip(files, result))

    # if simulate, only print result
    if simulate:
        print('Simulated results:')
        for key, val in dictionary:
            simulate(key, val)
    # else print result and rename
    else:
        print('Renaming:')
        for key, val in dictionary:
            simulate(key, val)
            rename(key, val)



"""
CLI utility that renames files in bulk in specified path, with support for datetime formating
"""

import click
import os
import piexif
import time
# import logging


@click.command()
@click.option('--path', prompt=True, help="Path to folder to run against")
@click.option('--recurse', '-r', is_flag=True, help="Recursivly renames ALL sub files in folder, please be careful!")
@click.option('--simulate', '-s', is_flag=True, help="Simulates results, writing changes to console without doing anything")
@click.option('--reverse', is_flag=True, help="Reverse order of renaming")
@click.option('--filter', '-f', type=str, help="Use a string or file ending to be included, example .jpg only includes jpg files")
@click.option('--rename', type=str, help="Use %Y:%m:%d:%H:%M datetime format or ### for incremental number, example newname###")
@click.option('--append', type=str, help="Adds input to end of filename, example input gray to file orange.txt becomes orangegray.txt")
@click.option('--ending', help="Replace filending to given format, example jpg changes all endings to .jpg")
@click.option('--remove', help="Remove entered string from all filenames")
@click.option('--replace', nargs=2, type=str, help="Replace x with y in filenames, use --replace x y makes regex.jpg to regey.jpg")
@click.option('--strip', help="Use none to remove whitespaces or a character to replace them with")
@click.option('--tofolder', nargs=2, help="Moves files matching x to folder named y, example .jpg pictures moves all jpg files to subfolder pictures")
@click.option('--lower', is_flag=True, help="Make all names lowercase")
@click.option('--upper', is_flag=True, help="Make all names uppercase")
@click.option('--exif', is_flag=True, help="Strips exif metadata from JPEG/TIFF images")
@click.option('--verbose', '-v', is_flag=True, help="Produces verbose output")


def main(path, recurse, exif, simulate, lower, upper, strip, rename, filter, verbose, ending, tofolder, append, replace, reverse, remove):
    '''
    # To be implemented
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    # create a file handler
    handler = logging.FileHandler('renamer.log')
    handler.setLevel(logging.INFO)
    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(handler)
    '''

    # get files from path if recurse
    if recurse:
        files = get_files_recurse(path, verbose)
    # else get files only in folder
    else:
        files = get_files(path, verbose)

    # check if reverse true, if so, reverse list
    if reverse:
        files.reverse()

    if filter:
        if verbose:
            click.echo('Filter {} given'.format(filter))
        filter_files(files, filter, verbose)

    if ending:
        if verbose:
            click.echo('--ending option given with {}'.format(ending))
        change_ending(files, ending, verbose)

    if replace:
        if verbose:
            click.echo('--replace option given with {} and {}'.format(replace[0], replace[1]))
        replace_(files, replace, verbose)

    if remove:
        if verbose:
            click.echo('--remove option given with {}'.format(remove))
        remove_match(files, remove, verbose)

    if tofolder:
        if verbose:
            click.echo('--tofolder option given with {} and {}'.format(tofolder[0], tofolder[1]))
        to_folder(files, tofolder, verbose)

    # check if strip exif
    if exif:
        if verbose:
            click.echo('--exif given, stripping exif metadata from jpg/tiff files')
        strip_exif(files)

    if append:
        if verbose:
            click.echo('--append option given with {}'.format(append))
        append_(files, append, verbose)

    if rename:
        if verbose:
            click.echo('--rename option given with {}'.format(rename))
        rename_custom(files, rename, verbose)

    if strip:
        if verbose:
            click.echo('--strip option given with {}'.format(strip))
        replace_space(files, strip, verbose)

    # check lower option
    if lower and not upper:
        if verbose:
            click.echo('Lower = True, running to lowercase')
        to_lowercase(files)

    # check upper option
    if upper and not lower:
        if verbose:
            click.echo('Upper = True, running to uppercase')
        to_uppercase(files)

    # error if both given
    if lower and upper:
        click.echo("You can't use both upper and lower")

    try:
        # check that there is a new name
        if files[0].newname:
            if simulate:
                if verbose:
                    click.echo('--simulate option given, no changes will be made')
                click.echo('Simulated results:')
            else:
                if verbose:
                    click.echo('no simulated option given, changes will be made to filenames')
                click.echo('Renaming:')
            rename_(files, simulate, verbose)
        else:
            click.echo('No action take as no new name was given')
    except IndexError:
        click.echo('No action take as no new name was given')


class File:
    def __init__(self, oldname, path):
        self.oldname = oldname
        self.newname = None
        self.path = path


def to_folder(files, tofolder, verbose):
    """
    moves files matching tofolder[0] to folder named tofolder[1]
    if folder does not exists it is created in subfolder of first file in files path
    :param files: list of file objects
    :param tofolder: tuple of string to match and name of subfolder
    :param verbose: indicates if verbose output should be written
    :return:
    """
    to_move = []
    for file in files:
            # check if filter is in old filename
            if tofolder[0] in file.oldname:
                if verbose:
                    click.echo('{} matched filter'.format(file.oldname))
                to_move.append(file)
            else:
                if verbose:
                    click.echo('{} did not match the filter'.format(file.oldname))
    # set path of subfolder using path of first file found in files
    if files[0]:
        newpath = files[0].path + os.sep + tofolder[1]
        if verbose:
            click.echo('New path set to {}'.format(newpath))
    else:
        click.echo('No files found to move')
        return

    # create folder to move to
    if not os.path.exists(newpath):
        if verbose:
            click.echo('{} not found, creating folder'.format(newpath))
        os.makedirs(newpath)

    # move files in list to new path
    for file in to_move:
        if verbose:
            click.echo('Moving {} to {}'.format(file.oldname, newpath))
        os.rename((file.path + os.sep + file.oldname), (newpath + os.sep + file.oldname))


def replace_(files, replace_tuple, verbose):
    """
    replaces replace_tuple[0] with replace_tuple[1] in file.newname
    :param files: list of file objects
    :param replace_tuple: tuple with 2 strings
    :param verbose: indicates if verbose output should be written
    :return:
    """
    for file in files:
        if replace_tuple[0] in file.oldname:
            file.newname = file.oldname.replace(replace_tuple[0], replace_tuple[1])
            if verbose:
                click.echo('{} found in {} and replaced by {} new name is {}'.format(replace_tuple[0], file.oldname, replace_tuple[1], file.newname))


def remove_match(files, remove, verbose):
    """
    removes match to string remove from file.oldname and stores in file.newname
    :param files: list of file objects
    :param remove: string to remove from filename
    :param verbose: indicates if verbose output should be written
    :return:
    """
    for file in files:
        if remove in file.oldname:
            file.newname = file.oldname.replace(remove, '')
            if verbose:
                click.echo('Removing {} from {} new name {}'.format(remove, file.oldname, file.newname))
        else:
            if verbose:
                click.echo('{} not found in {}'.format(remove, file.oldname))


def append_(files, append, verbose):
    """
    appends string append to file.oldname and stores in file.newname
    :param files: list of file objects
    :param append: string with text to append
    :param verbose: indicates if verbose output should be written
    :return:
    """
    for file in files:
        if '.' in file.oldname:
            file.newname = file.oldname.split('.')[0] + append + '.' + file.oldname.split('.')[1]
            if verbose:
                click.echo('File ending found in {}, new name is {}'.format(file.oldname, file.newname))
        else:
            file.newname = file.oldname + append
            if verbose:
                click.echo('No file ending found in {}, new name is {}'.format(file.oldname, file.newname))


def change_ending(files, ending, verbose):
    """
    alters file ending of files
    if ending exists it is replaces, otherwise it is added
    :param files: list of file objects
    :param ending: string representing file ending, with or without .
    :param verbose: indicates if verbose output should be written
    :return:
    """
    # make sure there are no dots in ending string
    try:
        file_ending = ending.split('.')[1]
    except IndexError:
        file_ending = ending
    for file in files:
        if '.' in file.oldname:
            if verbose:
                click.echo('Filending {} found in {} changing to {}'.format(('.' + file.oldname.split('.')[1]), file.oldname, file_ending))
            file.newname = file.oldname.split('.')[0] + '.' + file_ending
        else:
            if verbose:
                click.echo('No filending found in {} adding {}'.format(file.oldname, file_ending))
            file.newname = file.oldname + '.' + file_ending


def strip_exif(files):
    """
    strips exif metadata from jpg or tiff files
    :param files: list with file objects
    :return: list with file objects
    """
    for file in files:
        try:
            if '.jpg' in file.oldname or '.tiff' in file.oldname:
                piexif.remove((file.path + file.oldname))
                click.echo('Metadata removed from {}'.format(file.oldname))
            else:
                click.echo('{} is not a JPEG or TIFF and wont be processed'.format(file.oldname))
        except Exception as e:
            click.echo(e)


def filter_files(files, filter, verbose):
    """
    removes antries from files list that does not contain
    filter string
    :param files: list of file objects
    :param filter: string used to filter files
    :param verbose: indicates if verbose output should be written
    :return:
    """
    # list for files to remove
    to_remove = []
    for file in files:
        # check if filter is in old filename
        if filter not in file.oldname:
            if verbose:
                click.echo('{} did not match filter'.format(file.oldname))
            to_remove.append(file)
        else:
            if verbose:
                click.echo('{} did match the filter'.format(file.oldname))
    for i in to_remove:
        if verbose:
            click.echo('Removing {} from list of files due to not matching filter'.format(i.oldname))
        files.remove(i)


def rename_custom(files, rename_, verbose):
    """
    set newname based on user input
    using pre-defined patterns for naming rules
    :param files: list of file objects
    :param rename_: user input string
    :param verbose: indicates if verbose output should be written
    """
    i = 1
    for file in files:
        if '.' in file.oldname:
            file.newname = rename_ + '.' + file.oldname.split('.')[1]
            if verbose:
                click.echo("A '.' was found in filename {} assuming file ending {}".format(file.oldname, ('.' + file.oldname.split('.')[1])))
        else:
            file.newname = rename_
            if verbose:
                click.echo('No filending was found in file {}'.format(file.oldname))

        if '#' in file.newname:
            # count number of # present
            count = file.newname.count('#')
            if verbose:
                click.echo('Found {} instances of # in user input'.format(count))
            # create a variable for the
            replace_ = '#' * count
            # create a variable for use in format based on count
            fill = '0' + str(count) + 'd'
            file.newname = file.newname.replace(replace_, format(i, fill))

        if '%Y' in rename_:
                try:
                    year = time.strftime("%Y")
                    file.newname = file.newname.replace('%Y', year)
                    if verbose:
                        click.echo('Found %Y in {} replacing with {}'.format(file.newname, year))
                except:
                    if verbose:
                        click.echo('Found no %Y in {}'.format(file.newname))
                    pass
        if '%m' in rename_:
                try:
                    month = time.strftime("%m")
                    file.newname = file.newname.replace('%m', month)
                    if verbose:
                        click.echo('Found %m in {} replacing with {}'.format(file.newname, month))
                except:
                    if verbose:
                        click.echo('Found no %m in {}'.format(file.newname))
                    pass

        if '%d' in rename_:
                try:
                    day = time.strftime("%d")
                    file.newname = file.newname.replace('%d', day)
                    if verbose:
                        click.echo('Found %d in {} replacing with {}'.format(file.newname, day))
                except:
                    if verbose:
                        click.echo('Found no %d in {}'.format(file.newname))
                    pass
        if '%H' in rename_:
                try:
                    hour = time.strftime("%H")
                    file.newname = file.newname.replace('%H', hour)
                    if verbose:
                        click.echo('Found %H in {} replacing with {}'.format(file.newname, hour))
                except:
                    if verbose:
                        click.echo('Found no %H in {}'.format(file.newname))
                    pass
        if '%M' in rename_:
                try:
                    minute = time.strftime("%M")
                    file.newname = file.newname.replace('%M', minute)
                    if verbose:
                        click.echo('Found %M in {} replacing with {}'.format(file.newname, minute))
                except:
                    if verbose:
                        click.echo('Found no %M in {}'.format(file.newname))
                    pass
        i = i + 1


def replace_space(files, char, verbose):
    """
    replaces spaces with custom character or removes them
    :param files: list of file objects
    :param char: character to replace space
    :param verbose: indicates if verbose output should be written
    """
    if char == 'none':
        char = ''
        if verbose:
            click.echo('Found no replacement character, will strip spaces completely')
    for file in files:
        file.newname = file.oldname.replace(' ', char)
        if verbose:
            click.echo('Replacing space with {} in {}'.format(char, file.oldname))


def get_files(folder_path, verbose):
    """
    gets files from folder
    :param folder_path: string representing a folder path
    :param verbose: indicates if verbose output should be written
    :return: list of file objects
    """
    f = []
    try:
        for (dirpath, dirnames, filenames) in os.walk(folder_path):
            for file in filenames:
                f.append(File(file, (dirpath + os.sep)))
                if verbose:
                    click.echo('Found file {} in {}'.format(file, dirpath))
            break
        return f
    except Exception as e:
        click.echo(e)
        return None


def to_uppercase(files):
    """
    sets newname to uppercase
    :param files: list of file objects
    """
    for file in files:
        file.newname = file.oldname.upper()


def to_lowercase(files):
    """
    sets newname to lowercase
    :param files: list of file objects
    """
    for file in files:
        file.newname = file.oldname.lower()


def get_files_recurse(folder_path, verbose):
    """
    gets files from folder and subfolders
    :param folder_path: string representing folder path
    :param verbose: indicates if verbose output should be written
    :return: list of file objects
    """
    paths = []
    try:
        for root, dirs, files in os.walk(folder_path):
            for name in files:
                paths.append(File(name, (root + os.sep)))
                if verbose:
                    click.echo('Found file {} in {}'.format(name, root))
        return paths
    except Exception as e:
        click.echo(e)
        return None


def rename_(files, simulate, verbose):
    """
    renames files from file.oldname to file.newname
    also checking if file already exists, if it does, it appends
    a 3 digit number to indicate iteration and prevent name conflict
    :param files: list of file objects
    :param simulate: boolean indicating if it should print only or print and rename
    :param verbose: indicates if verbose output should be written
    :return:
    """
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
            click.echo('{} renamed to {}'.format(file.oldname, file.newname))

        except WindowsError as e:
            # if error is file already exist
            if e.errno == 17:
                if verbose:
                    click.echo('File {} already exists, adding additional numbers to filename'.format(file.newname))
                # check if file has a file ending
                if '.' in file.newname:
                    # store filending in variable
                    fileending = '.' + file.newname.split('.')[1]
                    if verbose:
                        click.echo('File {} has filending {}'.format(file.newname, fileending))
                    # if not simulating, rename
                    if not simulate:
                        # rename using filending, appending 3 digit value based on i
                        os.rename((file.path + file.oldname), (file.path + file.newname.split('.')[0] + '-' + format(i, '02d') + fileending))
                    click.echo('{} renamed to {}'.format(file.oldname, (file.newname.split('.')[0] + '-' + format(i, '02d') + fileending)))
                else:
                    if verbose:
                        click.echo('File {} has no filending'.format(file.newname))
                    # rename without filending,  appending 3 digit value based on i
                    os.rename((file.path + file.oldname),
                              (file.path + file.newname.split('.')[0] + '-' + format(i, '02d')))
                    click.echo('{} renamed to {}'.format(file.oldname, (file.newname.split('.')[0] + '-' + format(i, '02d'))))
            else:
                # error was not file exists, print it
                click.echo(e.winerror)
        last = file.newname
        i = i + 1


if __name__ == '__main__':
    main()
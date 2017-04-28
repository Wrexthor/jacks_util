import click
import re

'''
takes a string as input, attempts to find a unit type in it and
convert it to other unit types
'''

@click.command()
@click.option('--input', '-i', help="String to convert")
@click.option('--decimals', '-d', default=2, help="Number of decimals to round to, defaults to 2")


def convert(input, decimals):
    unit = get_unit(input)
    fail = False
    if not unit:
        click.echo('Found no Unit to convert in text, please try again')
        fail = True
    number = get_number(input)
    if not number:
        click.echo('Found no number to convert in text, please try again')
        fail = True

    if not fail:
        if unit == 1:
            # run to pound conversion
            result = convert_from_kg(number, decimals)
        elif unit == 2:
            # run to kg conversion
            result = convert_from_pounds(number, decimals)
        elif unit == 3:
            result = convert_from_ounce(number, decimals)
        else:
            result = None
        click.echo(result)


def convert_from_kg(number, decimal):
    pound = round((number * 2.20462), decimal)
    gram = round((number * 1000), decimal)
    ounce = round((number * 35.2739619496), decimal)
    number = round(number, decimal)
    click.echo('{}Kg equals {}pounds, {}grams or {}ounces'.format(number, pound, gram, ounce))



def convert_from_ounce(number, decimal):
    kg = round((number / 35.274), decimal)
    pound = round((number * 0.0625), decimal)
    gram = round((number / 0.035274), decimal)
    number = round(number, decimal)
    click.echo('{}ounce equals {}Kg, {}grams or {}pounds'.format(number, kg, gram, pound))


def convert_from_pounds(number, decimal):
    kg = round((number / 2.20462), decimal)
    gram = round(((number / 2.20462) * 1000), decimal)
    ounce = round((number * 16.000), decimal)
    number = round(number, decimal)
    click.echo('{}pounds equals {}Kg, {}grams or {}ounces'.format(number, kg, gram, ounce))



def get_number(text):
    number = re.search(r'\d+', text).group()
    click.echo('The number {} found in text'.format(number))  # debug
    return float(number)


def find_word(text, word):
    # replace with an awesome regex to avoid getting weird matches for short abbrevations like L
    # regex finding word trailing a space
    #space = re.search('\d|(?<= )\w+\b', word)
    # regex looking for digit or space before word, does not work AT ALL!
    # result = re.search('\b|\d%s' % word, text)
    if word in text:
        return True
    else:
        return False


def get_unit(text):
    mass = {'kg': 1, 'kilo': 1, 'kilogram': 1, 'kilogramme': 1, 'pound': 2, 'lb': 2, 'lbs': 2, "lb's": 2, 'ounce': 3, 'oz': 3}
    length = {'m': 4, 'metre': 4, 'meter': 4, 'inch': 5, 'in': 5, 'feet': 6, 'foot': 6, 'ft': 6, 'yard': 7, 'yd': 7, 'mile': 8, 'Km': 9, 'kilometer': 9}
    volume = {'millilitre': 10, 'ml': 10, 'litre': 11, 'liter': 11, 'l': 11, 'pint': 12, 'pt': 12, 'gallon': 13, 'gal': 13}

    # merge dicts for iteration
    units = mass.copy()
    units.update(length)
    units.update(volume)

    for key, val in units.items():
        if find_word(text, key):
            click.echo('The unit {} found in text'.format(key))  # debug
            return val



if __name__ == '__main__':
    convert()
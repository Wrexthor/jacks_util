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
            result = None
        else:
            result = None
        click.echo(result)


def convert_from_kg(number, decimal):
    pound = round((number * 2.20462), decimal)
    gram = round((number * 1000), decimal)
    ounce = round((number * 35.2739619496), decimal)
    click.echo('Multiplying {} with 2.20462'.format(number))  # debug
    number = round(number, decimal)
    click.echo('{}Kg equals {}pounds, {}grams or {}ounces'.format(number, pound, gram, ounce))



def convert_from_pounds(number, decimal):
    kg = round((number / 2.20462), decimal)
    gram = round(((number / 2.20462) * 1000), decimal)
    ounce = round((number * 16.000), decimal)
    click.echo('Dividing {} with 2.2046'.format(number))  # debug
    number = round(number, decimal)
    click.echo('{}pounds equals {}Kg, {}grams or {}ounces'.format(number, kg, gram, ounce))



def get_number(text):
    number = re.search(r'\d+', text).group()
    #number = filter(str.isdigit, text)
    click.echo('The number {} found in text'.format(number))
    return float(number)


def find_word(text, word):
    if word in text:
        return True
    else:
        return False


def get_unit(text):
    mass = {'kg': 1, 'kilo': 1, 'kilogram': 1, 'kilogramme': 1, 'pound': 2, 'lb': 2, 'lbs': 2, "lb's": 2, 'ounce': 3, 'oz': 3}
    length = {'m': 1, 'metre': 1, 'meter': 1, 'inch': 2, 'in': 2}

    for key, val in mass.items():
        if find_word(text, key):
            click.echo('The unit {} found in text'.format(key))
            return val



if __name__ == '__main__':
    convert()
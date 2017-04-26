import click
import re

'''
takes a string as input, attempts to find a unit type in it and
convert it to other unit types
'''

@click.command()
@click.option('--input', '-i', help="String to convert")


def convert(input):
    unit = get_unit(input)
    number = get_number(input)

    if unit == 1:
        # run to pound conversion
        result = convert_to_pound(number)
    elif unit == 2:
        # run to kg conversion
        result = convert_to_kg(number)
    elif unit == 3:
        pass
    else:
        pass
    click.echo(result)

def convert_to_pound(number):
    return number * 2.20462


def convert_to_kg(number):
    return number / 0.454


def get_number(text):
    number = re.search(r'\d+', text).group()
    #number = filter(str.isdigit, text)
    return float(number)


def find_whole_word(text):
    return re.compile(r'\b({0})\b'.format(text), flags=re.IGNORECASE).search


def get_unit(text):
    mass = {'kg': 1, 'kilo': 1, 'kilogram': 1, 'kilogramme': 1, 'pound': 2, 'lb': 2, 'lbs': 2, "lb's": 2}
    length = {'m': 1, 'metre': 1, 'meter': 1, 'inch': 2, 'in': 2}

    for key, val in mass.items():
        find_whole_word(key)
        return val



if __name__ == '__main__':
    convert()
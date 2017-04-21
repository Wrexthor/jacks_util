import click
import string
import random
import pyperclip


@click.command()
@click.option('--char', '-c', is_flag=True, help="Use special characters in password")
@click.option('--length', '-l', default=8, help="Length of the generated password, defaults to 8 characters")
@click.option('--upper', '-u',  default=False, is_flag=True, help="Makes password "
                                                                  "all uppercase, default is all lowercase")
@click.option('--number', '-n',  default=False, is_flag=True, help="Adds numbers to passwords")
@click.option('--mix', '-m',  default=False, is_flag=True, help="Makes password a mix of upper and lowercase")
@click.option('--clip', '-cl', default=False, is_flag=True, help="Outputs password to clipboard, defaults to false")

def pwgen(length, char, upper, mix, clip, number):
    if upper:
        chars = string.ascii_uppercase
    elif mix:
        chars = string.ascii_letters
    else:
        chars = string.ascii_lowercase

    if number:
        chars = chars + string.digits

    if char:
        chars = chars + string.punctuation

    pw = ''.join(random.choice(chars) for _ in range(length))
    click.echo(pw)
    if clip:
        pyperclip.copy(pw)
        click.echo('Password copied to clipboard')

if __name__ == '__main__':
    pwgen()



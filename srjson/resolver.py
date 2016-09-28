
from getpass import getpass


def prompt(s):

    value = raw_input(s)

    return value


def default_resolver(action, parent_path=''):

    if action == 'PASSWORD':
        value = getpass.getpass("Enter password for '{}': ".format(parent_path))
        return value

    if action == 'PROMPT':
        value = prompt("Enter value for '{}': ".format(parent_path))
        return value

    return '|NO_ACTION_RESOLVER:{}|'.format(action)

import logging
import subprocess
import argparse


def login():
    """
    This function parses the command line arguments and logins to the registry
    with provided username and password.
    """

    # Parsing command line arguments.
    parser = argparse.ArgumentParser(
        description='Loading images required for running k8s tests.')
    parser.add_argument('-r', '--registry', help='Specify the image registry')
    parser.add_argument('-u', '--username', help='Set the username')
    parser.add_argument('-p', '--password', help='Set the password')
    args = parser.parse_args()
    if not (args.registry and args.username and args.password):
        print('Please specify the registry, username and password.')
        return False, None, None, None
    # Logging to image registry.
    logging.debug('Logging to daocloud registry')
    success = subprocess.call(['docker', 'login', args.registry,
                               '-u', args.username, '-p', args.password])
    if success != 0:
        return False, None, None, None
    return True, args.registry, args.username, args.password

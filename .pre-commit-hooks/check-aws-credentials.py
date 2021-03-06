#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import Python libs
import json
import argparse


def check_for_credentials(data, disallowed_keys_with_values):
    errors = set()
    for key, value in data.items():
        if key in disallowed_keys_with_values:
            errors.add(key)
        if isinstance(value, dict):
            for error in check_for_credentials(value, disallowed_keys_with_values):
                errors.add(error)
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-k', '--key',
        dest='keys',
        metavar='KEY',
        action='append',
        default=[
            'aws_access_key',
            'aws_secret_key'
        ]
    )
    parser.add_argument('files', nargs='+')

    args = parser.parse_args()
    if not args.files:
        parser.exit('No files were passed in')

    collected_errors = {}
    for fname in args.files:
        try:
            with open(fname) as rfh:
                data = json.loads(rfh.read())
        except ValueError:
            parser.exit('Failed to JSON load {}'.format(fname))
        errors = check_for_credentials(data, args.keys)
        if errors:
            collected_errors[fname] = errors

    if collected_errors:
        for fname, errors in collected_errors.items():
            print('Found a populated secret key value in {}:'.format(fname))
            for error in errors:
                print('  - {}'.format(error))
        parser.exit(1)


if __name__ == "__main__":
    main()

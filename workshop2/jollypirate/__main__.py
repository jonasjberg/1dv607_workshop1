# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se

import argparse
import logging
import sys

import jollypirate


def init_argparser():
    parser = argparse.ArgumentParser(
        prog='jollypirate',
        description='Boat Club Management Suite',
        epilog='.. PIRATES!',
        add_help=False
    )

    parser.add_argument(
        '-h', '--help',
        action='help',
        help='Show this help message and exit.'
    )

    optgrp_output = parser.add_mutually_exclusive_group()
    optgrp_output.add_argument(
        '--debug',
        dest='debug',
        action='store_true',
        default=False,
        help='Enables debug mode, prints detailed debug information.'
    )
    optgrp_output.add_argument(
        '-v', '--verbose',
        dest='verbose',
        action='store_true',
        default=False,
        help='Enables verbose mode, prints additional information.'
    )

    return parser


def init_logging(args):
    """
    Configures the log format and logging settings.

    Args:
        args: Parsed option arguments as type 'argparse.NameSpace'.
    """
    _date_format = '%Y-%m-%d %H:%M:%S'
    if args.debug:
        fmt = '%(levelname)s %(name)-25.25s %(funcName)-20.20s  %(message)s'
        logging.basicConfig(
            level=logging.DEBUG, format=fmt, datefmt=_date_format
        )
    elif args.verbose:
        fmt = '%(levelname)s %(message)s'
        logging.basicConfig(
            level=logging.INFO, format=fmt, datefmt=_date_format
        )
    else:
        fmt = '%(levelname)s %(message)s'
        logging.basicConfig(
            level=logging.WARNING, format=fmt
        )


def _parse_args(raw_args):
    """
    Parses the given option arguments with argparse.

    Args:
        raw_args: The option arguments to parse as a list of strings.

    Returns:
        Parsed option arguments as type 'argparse.NameSpace'.
    """
    parser = init_argparser()
    return parser.parse_args(args=raw_args)


def parse_args(raw_args):
    """
    Parses raw positional arguments.

    Parses the given option arguments with argparse and verifies legality of
    any combinations.

    Args:
        raw_args: The option arguments as a list of strings.

    Returns:
        Parsed option arguments as type 'argparse.NameSpace'.
    """
    args = _parse_args(raw_args)
    init_logging(args)
    return args


def main(args):
    opts = parse_args(args)
    init_logging(opts)

    app = jollypirate.application()
    app.run()


if __name__ == '__main__':
    main(sys.argv[1:])

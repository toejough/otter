"""stdout interactor."""

import sys


def write(data):
    """write the data to stdout."""
    sys.stdout.write(data)
    sys.stdout.flush()


def reset():
    """reset the output."""
    write('\n')

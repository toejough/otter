"""stderr interactor."""

import sys


# record early, because this most likely will get replaced.
WRITE = sys.stderr.write


def write(data):
    """write the data to stderr."""
    output = WRITE(data)
    sys.stderr.flush()
    return output


def reset():
    """reset the output."""
    write('\n')


def is_reset(prior_data):
    """return whether the prior data indicates a reset was done last."""
    return prior_data and prior_data.endswith('\n')
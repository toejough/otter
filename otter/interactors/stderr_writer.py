"""stderr interactor."""


# [ Import ]
import sys


# [ Globals ]
# record early, because this most likely will get replaced.
_WRITE = sys.stderr.write


# [ Public ]
def write(data):
    """write the data to stderr."""
    output = _WRITE(data)
    sys.stderr.flush()
    return output


def reset():
    """reset the output."""
    write('\n')


def combine(prior_data, new_data):
    """combine two hunks of data."""
    return prior_data + new_data

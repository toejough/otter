"""stderr interactor."""


# [ Import ]
# [ -Python ]
import sys
# [ -Project ]
from . import mem_recorder


# [ Globals ]
# record early, because this most likely will get replaced.
_WRITE = sys.stderr.write
_RECORDER = mem_recorder.get_recorder()


# [ Public ]
def write(data, *, from_stream=False):
    """write the data to stdout."""
    output = _WRITE(data)
    sys.stderr.flush()
    _RECORDER.record(data, from_stream=from_stream)
    return output


def reset():
    """reset the output."""
    if not _RECORDER.is_reset():
        write('\n')


def combine(prior_data, new_data):
    """combine two hunks of data."""
    return prior_data + new_data


last_output_matches = _RECORDER.last_output_matches
is_reset = _RECORDER.is_reset
record = _RECORDER.record


def last_from_stream():
    """Return whether the last output was from a stream."""
    return _RECORDER.last_from_stream

"""
API Layer.

Translation from how I want users to be able to use the library to the
core actions performed.
"""


import sys
import functools
from . import app
from .interactors import stdout_writer, stderr_writer, mem_recorder


STATE = {}


class Stream:
    """Stream."""

    def __init__(
        self, *,
        write_interactor=stdout_writer,
        recorder_interactor=mem_recorder
    ):
        """init the state."""
        # initial state.
        self.data = ''

        # set interactors
        self._write = functools.partial(
            app.write_from_stream,
            write_interactor=write_interactor,
            recorder_interactor=recorder_interactor,
        )

    def write(self, data):
        """
        write the data.

        Rewrite data from a new line if the stream's data is not the last output
        recorded.
        """
        output = self._write(self.data, data)
        # update the stream data
        self.data += data
        # return what the writer returned
        return output


def replace(parent, func_name, *, write_interactor=stdout_writer, recorder_interactor=mem_recorder):
    """watch the output."""
    # get functions replaced in the given parent
    replaced = STATE.get(parent, {})
    # if this function is replaced, restore it before re-replacing
    if func_name in replaced:
        original = replaced[func_name]['original']
        setattr(parent, func_name, original)
    # get the original function
    func = getattr(parent, func_name)
    # replace the function
    setattr(
        parent, func_name,
        functools.wraps(func)(functools.partial(
            app.write_interruption,
            write_interactor=write_interactor,
            recorder_interactor=recorder_interactor,
        ))
    )
    # save the original and the replacement
    replaced[func_name] = {
        'original': func,
        'replacement': replaced
    }
    # update the global state
    STATE[parent] = replaced


def replace_stds():
    """replace the std streams."""
    replace(sys.stdout, 'write', write_interactor=stdout_writer)
    replace(sys.stderr, 'write', write_interactor=stderr_writer)

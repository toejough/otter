"""
Library API.

This is how the user should interact with the library.

The intent is to be a simple-to-use overlay of the purely functional application code.
The translation is from easy use to required actions for each function.
State and some simple logic is allowed.
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
            app.write,
            write_interactor=write_interactor,
            recorder_interactor=recorder_interactor,
        )
        self._output_ends_with = functools.partial(
            app.output_ends_with,
            recorder_interactor=recorder_interactor,
        )
        self._reset = functools.partial(
            app.reset,
            write_interactor=write_interactor,
            recorder_interactor=recorder_interactor,
        )

    def write(self, data):
        """
        write the data.

        Rewrite data from a new line if the stream's data is not the last output
        recorded.
        """
        # if the last recorded output matches
        if self._output_ends_with(self.data):
            # write the new data
            output = self._write(data)
        else:
            # reset the writer if there's really data to writ
            if data:
                self._reset()
            # write the old data, then the new data
            output = self._write(self.data + data)
        # update the stream data
        self.data += data
        # return what the writer returned
        return output


def replace(parent, func_name, write_interactor, *, recorder_interactor=mem_recorder):
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
    app.replace(
        parent, func_name, write_interactor,
        recorder_interactor=recorder_interactor
    )
    # save teh original and the replacement
    replaced[func_name] = {
        'original': func,
        'replacement': replaced
    }
    # update the global state
    STATE[parent] = replaced


def replace_stds():
    """replace the std streams."""
    replace(sys.stdout, 'write', stdout_writer)
    replace(sys.stderr, 'write', stderr_writer)

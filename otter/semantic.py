"""Semantic interactions with the library."""


import sys
from . import app
from .interactors import stdout_writer, stderr_writer


STATE = {}


class Stream:
    """Stream."""

    def __init__(self):
        """init the state."""
        self.data = ''
        self.write_interactor = stdout_writer

    def write(self, data):
        """
        write the data.

        Rewrite data from a new line if the stream's data is not the last output from any of the watched outputs.
        """
        if data:
            self._write(data)

    def _write(self, data):
        """
        Actually write the data.

        Differs from self.write in that this does not filter out falsy input.
        """
        recorded_output = app.get_recorded_output()
        if self.data and recorded_output and recorded_output.endswith(self.data):
            app.write(data, write_interactor=self.write_interactor)
        else:
            if not app.is_reset(write_interactor=self.write_interactor):
                app.reset(write_interactor=self.write_interactor)
            app.write(self.data + data, write_interactor=self.write_interactor)
        self.data += data


def replace(parent, func_name, write_interactor):
    """watch the output."""
    replaced = STATE.get(parent, [])
    if func_name not in replaced:
        app.replace(parent, func_name, write_interactor)
        replaced.append(func_name)
        STATE[parent] = replaced


def replace_stds():
    """replace the std streams."""
    replace(sys.stdout, 'write', stdout_writer)
    replace(sys.stderr, 'write', stderr_writer)

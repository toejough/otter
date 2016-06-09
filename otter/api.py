"""
API Layer.

Translation from how I want users to be able to use the library to the
core actions performed.
"""


import sys
from . import app
from .interactors import stdout_writer, stderr_writer, mem_recorder


STATE = {}
DEFAULT_RECORDER = mem_recorder.Recorder()


class Stream:
    """Stream."""

    def __init__(
        self, *,
        write_interactor=stdout_writer,
        recorder_interactor=DEFAULT_RECORDER
    ):
        """init the state."""
        # initial state.
        self.data = ''
        self._write_interactor = write_interactor
        self._recorder_interactor = recorder_interactor

    # [ App ]
    def _should_restart_stream(self, data, last_output_matches):
        """return whether the stream should be restarted."""
        return app.should_restart_stream(data, last_output_matches)

    # [ Interactors ]
    def _get_new_stream_data(self, prior_data, new_data):
        """Return the new stream data."""
        return self._write_interactor.combine(prior_data, new_data)

    def _last_output_matches(self, data):
        """return whether the last recorded output matches the stream."""
        return self._recorder_interactor.last_output_matches(data)

    def _write(self, data_to_write, should_reset):
        """actually write and record the data."""
        if should_reset and not self._recorder_interactor.is_reset():
            self._write_interactor.reset()
            self._recorder_interactor.record_reset()
        self._recorder_interactor.record(data_to_write, from_stream=True)
        return self._write_interactor.write(data_to_write)

    # [ Internal ]
    def write(self, data):
        """
        write the data.

        Rewrite data from a new line if the stream's data is not the last output
        recorded.
        """
        # Gather all the required data
        last_output_matches = self._last_output_matches(self.data)
        new_stream_data = self._get_new_stream_data(self.data, data)
        should_restart_stream = self._should_restart_stream(data, last_output_matches)
        data_to_write = new_stream_data if should_restart_stream else data

        # update the stream data
        self.data = new_stream_data

        # Write
        return self._write(data_to_write, should_restart_stream)


def replace(parent, func_name, *, write_interactor=stdout_writer, recorder_interactor=DEFAULT_RECORDER):
    """watch the output."""
    def _should_reset(data, last_from_stream):
        """return whether we should reset the output."""
        return app.should_reset_before_interruption(data, last_from_stream)

    def _last_output_from_stream():
        """Return whether the last output was from a stream."""
        return recorder_interactor.last_from_stream

    def _write(data, should_reset):
        """Actually write the data."""
        if should_reset and not recorder_interactor.is_reset():
            write_interactor.reset()
            recorder_interactor.record_reset()
        recorder_interactor.record(data, from_stream=False)
        return write_interactor.write(data)

    def write(data):
        """write the data."""
        # Data
        last_from_stream = _last_output_from_stream()
        should_reset = _should_reset(data, last_from_stream)

        # IO
        return _write(data, should_reset)

    def _get_original(parent, func_name):
        """get the original function."""
        # get functions replaced in the given parent
        replacements_in_parent = STATE.get(parent, {})
        func_replacement_data = replacements_in_parent.get(func_name, {})
        current_func = getattr(parent, func_name)
        return func_replacement_data.get('original', current_func)

    def _save_replacement(parent, func_name, original, write):
        # save the original and the replacement
        replacements_in_parent = STATE.get(parent, {})
        replacements_in_parent[func_name] = {
            'original': original,
            'replacement': write
        }
        # update the global state
        STATE[parent] = replacements_in_parent

    def _replace_function(parent, func_name, replacement):
        """replace the function."""
        setattr(parent, func_name, write)

    # get data
    original = _get_original(parent, func_name)

    # save replacement
    _save_replacement(parent, func_name, original, write)

    # replace the function
    _replace_function(parent, func_name, write)


def replace_stds():
    """replace the std streams."""
    replace(sys.stdout, 'write', write_interactor=stdout_writer)
    replace(sys.stderr, 'write', write_interactor=stderr_writer)

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
        self.write_interactor = write_interactor
        self.recorder_interactor = recorder_interactor

    def _should_restart_stream(self, data, last_output_matches):
        """return whether the stream should be restarted."""
        return app.should_restart_stream(data, last_output_matches)

    def _get_new_stream_data(self, data):
        """Return the new stream data."""
        return self.write_interactor.combine(self.data, data)

    def _last_output_matches(self):
        """return whether the last recorded output matches the stream."""
        return self.recorder_interactor.last_output_matches(self.data)

    def _write(self, data_to_write, should_reset):
        """actually write and record the data."""
        if should_reset and not self.recorder_interactor.is_reset():
            self.write_interactor.reset()
            self.recorder_interactor.record_reset()
        self.recorder_interactor.record(data_to_write, from_stream=True)
        return self.write_interactor.write(data_to_write)

    def write(self, data):
        """
        write the data.

        Rewrite data from a new line if the stream's data is not the last output
        recorded.
        """
        # Gather all the required data
        last_output_matches = self._last_output_matches()
        new_stream_data = self._get_new_stream_data(data)
        should_restart_stream = self._should_restart_stream(data, last_output_matches)
        data_to_write = new_stream_data if should_restart_stream else data

        # update the stream data
        self.data = new_stream_data

        # Write
        return self._write(data_to_write, should_restart_stream)


def replace(parent, func_name, *, write_interactor=stdout_writer, recorder_interactor=DEFAULT_RECORDER):
    """watch the output."""
    # get functions replaced in the given parent
    replaced = STATE.get(parent, {})
    # if this function is replaced, restore it before re-replacing
    if func_name in replaced:
        original = replaced[func_name]['original']
        setattr(parent, func_name, original)
    # get the original function
    func = getattr(parent, func_name)

    def _reset(data):
        """reset the output state so that new data is obviously new."""
        if app.should_reset_before_interruption(
            data,
            recorder_interactor.last_from_stream
        ) and not recorder_interactor.is_reset():
            write_interactor.reset()
            recorder_interactor.record_reset()

    def write(data):
        """write the data."""
        _reset(data)
        output = write_interactor.write(data)
        recorder_interactor.record(data, from_stream=False)

        # return what the writer returned
        return output

    # replace the function
    setattr(parent, func_name, write)
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

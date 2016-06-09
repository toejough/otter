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

    def _reset(self):
        """reset the output state so that a new stream is obviously new."""
        if not self.recorder_interactor.is_reset():
            self.write_interactor.reset()
            self.recorder_interactor.record_reset()

    def write(self, data):
        """
        write the data.

        Rewrite data from a new line if the stream's data is not the last output
        recorded.
        """
        if app.restart_stream(data, self.recorder_interactor.last_output_matches(self.data)):
            self._reset()
            output = self.write_interactor.write(self.data + data)
            self.recorder_interactor.record(self.data + data, from_stream=True)
        else:
            output = self.write_interactor.write(data)
            self.recorder_interactor.record(data, from_stream=True)

        # update the stream data
        self.data += data
        # return what the writer returned
        return output


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

"""
API Layer.

Translation from how I want users to be able to use the library to the
core actions performed.
"""


# [ Import ]
# [ -Python ]
import sys
# [ -Project ]
from . import app
from .interactors import stdout_writer, stderr_writer, mem_recorder


# [ Globals ]
_REPLACED_FUNCTIONS = {}
_DEFAULT_RECORDER = mem_recorder.Recorder()


# [ Public ]
class Stream:
    """Stream."""

    def __init__(
        self, *,
        write_interactor=stdout_writer,
        recorder_interactor=_DEFAULT_RECORDER
    ):
        """init the state."""
        # initial state.
        self.data = ''
        self._write_interactor = write_interactor
        self._recorder_interactor = recorder_interactor

    # [ Public ]
    # [ -Internal ]
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

    # [ Private ]
    # [ -App ]
    def _should_restart_stream(self, data, last_output_matches):
        """return whether the stream should be restarted."""
        return app.should_restart_stream(data, last_output_matches)

    # [ -Interactors ]
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


def replace_stds():
    """replace the std streams."""
    replace(sys.stdout, 'write', write_interactor=stdout_writer)
    replace(sys.stderr, 'write', write_interactor=stderr_writer)


def replace(parent, func_name, *, write_interactor=stdout_writer, recorder_interactor=_DEFAULT_RECORDER):
    """watch the output."""
    _save_original(parent, func_name)
    write = InterruptionWriter(write_interactor, recorder_interactor)
    setattr(parent, func_name, write)


class InterruptionWriter:
    """Interruption Writer."""

    def __init__(self, write_interactor, recorder_interactor):
        """Build an interruption function."""
        self._write_interactor = write_interactor
        self._recorder_interactor = recorder_interactor

    # [ Public ]
    # [ -Internal ]
    def __call__(self, data):
        """write the data."""
        # Data
        last_from_stream = self._last_output_from_stream()
        should_reset = self._should_reset_before_interruption(data, last_from_stream)

        # IO
        return self._write(data, should_reset)

    # [ Private ]
    # [ -App ]
    def _should_reset_before_interruption(self, data, last_from_stream):
        """return whether we should reset the output."""
        return app.should_reset_before_interruption(data, last_from_stream)

    # [ -Interactor ]
    def _last_output_from_stream(self):
        """Return whether the last output was from a stream."""
        return self._recorder_interactor.last_from_stream

    def _write(self, data, should_reset):
        """Actually write the data."""
        if should_reset and not self._recorder_interactor.is_reset():
            self._write_interactor.reset()
            self._recorder_interactor.record_reset()
        self._recorder_interactor.record(data, from_stream=False)
        return self._write_interactor.write(data)


# [ Private ]
# [ -Module Private ]
def _save_original(parent, func_name):
    """Save the original function."""
    originals = _get_replaced_functions()
    originals_in_parent = originals.get(parent, {})
    originals_in_parent[func_name] = _get_original_func(parent, func_name)
    originals[parent] = originals_in_parent


def _get_original_func(parent, func_name):
    """get the original function."""
    originals_in_parent = _get_replaced_functions().get(parent, {})
    current_func = getattr(parent, func_name)
    return originals_in_parent.get(func_name, current_func)


# [ -Global ]
def _get_replaced_functions():
    """Get the replacement data."""
    return _REPLACED_FUNCTIONS

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
from .interactors.output import StdOutOutputMechanism, StdErrOutputMechanism, Recorder, OutputDevice


# [ Globals ]
_REPLACED_FUNCTIONS = {}

_OUTPUT_DEVICE = OutputDevice()
_RECORDER = Recorder('')
_STD_OUT = StdOutOutputMechanism()
_STD_ERR = StdErrOutputMechanism()


# [ Public ]
class Stream:
    """Stream."""

    def __init__(self):
        """init the state."""
        # initial state.
        self.data = ''

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
        new_stream_data = self._get_updated_data(data)
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
    def _last_output_matches(self, data):
        """return whether the last recorded output matches the stream."""
        return _RECORDER.last_output == data

    def _write(self, data_to_write, should_reset):
        """actually write and record the data."""
        if should_reset:
            _OUTPUT_DEVICE.reset()
        output = _OUTPUT_DEVICE.write(data_to_write, _STD_OUT)
        _RECORDER.last_output = self.data
        _RECORDER.last_from_stream = True
        return output

    # [ -Data ]
    def _get_updated_data(self, new_data):
        """return the stream data, updated with the new data."""
        return self.data + new_data


def replace_stds():
    """replace the std streams."""
    replace(sys.stdout, 'write')
    # replace(sys.stderr, 'write')


def replace(parent, func_name):
    """watch the output."""
    _save_original(parent, func_name)
    write = InterruptionWriter().write
    setattr(parent, func_name, write)


class InterruptionWriter:
    """Interruption Writer."""

    # [ Public ]
    # [ -Internal ]
    def write(self, data):
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
        return _RECORDER.last_from_stream

    def _write(self, data, should_reset):
        """Actually write the data."""
        if should_reset:
            _OUTPUT_DEVICE.reset()
        output = _OUTPUT_DEVICE.write(data, _STD_OUT)
        _RECORDER.last_output = data
        _RECORDER.last_from_stream = False
        return output


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

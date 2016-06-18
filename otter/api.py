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

    def __init__(self, *, output_device=_OUTPUT_DEVICE):
        """init the state."""
        # initial state.
        self._data = ''
        self._output_device = output_device

    # [ Public ]
    # [ -Internal ]
    def write(self, data):
        """
        write the data.

        Rewrite data from a new line if the stream's data is not the last output
        recorded.

        """
        # This should be the only function which reads or writes the internal data field

        # update the stream data
        self._data = self._get_updated_data(self._data, data)

        # Write
        self._output_device.write(self._data)

    # [ -Data ]
    def _get_updated_data(self, existing_data, new_data):
        """return the stream data, updated with the new data."""
        return existing_data + new_data


def replace_stds():
    """replace the std streams."""
    replace(sys.stdout, 'write')
    # replace(sys.stderr, 'write', _STD_ERR)


def replace(parent, func_name, *, output_device=_OUTPUT_DEVICE):
    """watch the output."""
    _save_original(parent, func_name)
    write = InterruptionWriter(output_device=output_device).write
    setattr(parent, func_name, write)


class InterruptionWriter:
    """Interruption Writer."""

    def __init__(self, *, output_device=_OUTPUT_DEVICE):
        """init the state."""
        # initial state.
        self._output_device = output_device

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
        return self._output_device.last_from_stream

    def _write(self, data, should_reset):
        """Actually write the data."""
        if should_reset:
            self._output_device.reset()
        output = self._output_device.old_write(data)
        self._output_device.last_output = data
        self._output_device.last_from_stream = False
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

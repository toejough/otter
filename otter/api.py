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
        """Write the stream to the output device."""
        self._data = self._get_updated_data(self._data, data)
        self._write(self._data)

    # [ -Data ]
    def _get_updated_data(self, existing_data, new_data):
        """return the stream data, updated with the new data."""
        return existing_data + new_data

    # [ -Interactors ]
    def _write(self, data):
        """Write the data to the output device."""
        self._output_device.write_stream(data)


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
        return self._output_device.write_interruption(data)


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

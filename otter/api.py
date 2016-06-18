"""
API Layer.

Translation from how I want users to be able to use the library to the
core actions performed.
"""


# [ Import ]
from .interactors.output import OutputDevice


# [ Public ]
class Stream:
    """Stream."""

    def __init__(self, *, output_device=OutputDevice()):
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

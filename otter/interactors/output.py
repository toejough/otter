"""Shared output base."""


# [ Import ]
# [ -Python ]
import sys


# [ Public ]
class OutputDevice:
    """The output device."""

    _write = sys.stdout.write
    _flush = sys.stdout.flush

    def __init__(self, initial_data=''):
        """Init the state."""
        self._is_reset = False
        self._last_output = initial_data
        self._last_from_stream = False

    def reset(self):
        """Reset the device."""
        if not self._is_reset:
            self.old_write('\n')

    def old_write(self, data):
        """Write data to the device via the given output mechanism."""
        self._write(data)
        self._flush()
        self._is_reset = data.endswith('\n')

    # [ Private ]
    # [ -Internal ]
    def write_stream(self, stream_data):
        """actually write and record the data."""
        last_output_matches = self._last_output and stream_data.startswith(self._last_output)
        if stream_data and not last_output_matches:
            self.reset()
        if last_output_matches:
            to_write = stream_data[len(self._last_output):]
        else:
            to_write = stream_data
        self.old_write(to_write)
        self._last_output = stream_data
        self._last_from_stream = True

    # [ Private ]
    # [ -Interactor ]
    def write_interruption(self, data):
        """Actually write the data."""
        # Data
        last_from_stream = self._last_from_stream

        if data and last_from_stream:
            self.reset()
        output = self.old_write(data)
        self._last_output = data
        self._last_from_stream = False
        return output

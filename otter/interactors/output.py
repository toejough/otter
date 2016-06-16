"""Shared output base."""


# [ Import ]
# [ -Python ]
import sys


# [ Public ]
class OutputDevice:
    """The output device."""

    _write = sys.stdout.write
    _flush = sys.stdout.flush

    def __init__(self):
        """Init the state."""
        self._is_reset = False

    def reset(self):
        """Reset the device."""
        if not self._is_reset:
            self._write('\n')
            self._flush()
            self._is_reset = True

    def write(self, data, output_mechanism):
        """Write data to the device via the given output mechanism."""
        output_mechanism.write(data)
        self._is_reset = data.endswith('\n')


class StdOutOutputMechanism:
    """The stdout output mechanism."""

    _write = sys.stdout.write
    _flush = sys.stdout.flush

    def write(self, data):
        """write the data."""
        output = self._write(data)
        self._flush()
        return output


class StdErrOutputMechanism:
    """The stderr output mechanism."""

    _write = sys.stderr.write
    _flush = sys.stderr.flush

    def write(self, data):
        """write the data."""
        output = self._write(data)
        self._flush()
        return output


class Recorder:
    """Record output data."""

    def __init__(self, initial_data):
        """init state."""
        self.last_output = initial_data
        self.last_from_stream = False

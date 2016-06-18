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
            self._write('\n')
            self._flush()
            self._is_reset = True

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
            stream_data = stream_data[len(self._last_output):]
        self.old_write(stream_data)
        self._last_output = stream_data
        self._last_from_stream = True

    # [ Private ]
    # [ -App ]
    def _should_reset_before_interruption(self, data, last_from_stream):
        """return whether we should reset the output."""
        return data and last_from_stream

    # [ -Interactor ]
    def _last_output_from_stream(self):
        """Return whether the last output was from a stream."""
        return self._last_from_stream

    def write_interruption(self, data):
        """Actually write the data."""
        # Data
        last_from_stream = self._last_output_from_stream()
        should_reset = self._should_reset_before_interruption(data, last_from_stream)

        if should_reset:
            self.reset()
        output = self.old_write(data)
        self._last_output = data
        self._last_from_stream = False
        return output


class StdOutOutputMechanism:
    """The stdout output mechanism."""

    _write = sys.stdout.write
    _flush = sys.stdout.flush

    def write(self, data):
        """write the data."""
        self._write(data)
        self._flush()


class StdErrOutputMechanism:
    """The stderr output mechanism."""

    _write = sys.stderr.write
    _flush = sys.stderr.flush

    def write(self, data):
        """write the data."""
        self._write(data)
        self._flush()


class Recorder:
    """Record output data."""

    def __init__(self, initial_data):
        """init state."""
        self.last_output = initial_data
        self.last_from_stream = False

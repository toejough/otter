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
        self.last_output = initial_data
        self.last_from_stream = False

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
    def write(self, stream_data):
        """actually write and record the data."""
        should_reset = self._should_restart_stream(stream_data, self._last_output_matches(stream_data))
        self._reset(should_reset)
        self._write_to_device(stream_data)
        self._record_stream_written(stream_data)

    # [ -Logic ]
    def _should_restart_stream(self, data_exists, last_output_matches_data):
        """return whether the stream should be restarted."""
        return data_exists and not last_output_matches_data

    # [ -Interactors ]
    def _last_output_matches(self, data):
        """return whether the last recorded output matches the stream."""
        return self.last_output and data.startswith(self.last_output)

    def _reset(self, should_reset):
        """reset if we should."""
        if should_reset:
            self.reset()

    def _write_to_device(self, data_to_write):
        """write to the device."""
        if self._last_output_matches(data_to_write):
            data_to_write = data_to_write[len(self.last_output):]
        self.old_write(data_to_write)

    def _record_stream_written(self, data):
        self.last_output = data
        self.last_from_stream = True


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
